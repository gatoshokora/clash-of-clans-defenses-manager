import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


defenses = []
league_list = []
editing_index = None
detail_indexes = []

detail_window = None
detail_listbox = None
summary_listbox = None

detail_league_combo = None
detail_season_entry = None
detail_date_entry = None
detail_layout_entry = None
detail_stars_combo = None
detail_destruction_entry = None
detail_trophy_entry = None
detail_army_entry = None

selected_league = None

#データを受け取って辞書を作る関数
def get_input_data():
  league = league_combo.get()
  season = season_entry.get()
  date = date_entry.get()
  layout_id = layout_entry.get()
  stars = int(stars_combo.get())
  try:
    destruction = int(destruction_entry.get())

  except ValueError:
    messagebox.showwarning("入力エラー", "破壊率は数字で入力してください")
    return

  try:
    trophy = int(trophy_entry.get())
    if (trophy < -1) or (1 <= trophy <= 7) or (40 < trophy) :
      messagebox.showwarning("入力エラー", "そのトロフィー数は存在しません")
      return
    
  except ValueError:
    messagebox.showwarning("入力エラー","数字を入力してください")
    return

  army = army_entry.get()

  defense = {"league":league,"season":season,"date":date,"layout_id":layout_id,"stars":stars,"destruction":destruction,"trophy":trophy,"army":army}
  return defense

#詳細画面からデータを受け取って辞書を作成する
def get_detail_input_data():
  league = detail_league_combo.get()
  season = detail_season_entry.get()
  date = detail_date_entry.get()
  layout_id = detail_layout_entry.get()
  stars = int(detail_stars_combo.get())
  try:
    destruction = int(detail_destruction_entry.get())

  except ValueError:
    messagebox.showwarning("入力エラー", "破壊率は数字で入力してください")
    return

  try:
    trophy = int(detail_trophy_entry.get())
    if (trophy < -1) or (1 <= trophy <= 7) or (40 < trophy) :
      messagebox.showwarning("入力エラー", "そのトロフィー数は存在しません")
      return
    
  except ValueError:
    messagebox.showwarning("入力エラー","数字を入力してください")
    return

  army = detail_army_entry.get() 

  defense = {"league":league,"season":season,"date":date,"layout_id":layout_id,"stars":stars,"destruction":destruction,"trophy":trophy,"army":army}
  return defense

#入力欄を空にする
def clear_entries():
  #league_combo.current(0)
  #season_entry.delete(0, tk.END)
  date_entry.delete(0,tk.END)
  #layout_entry.delete(0,tk.END)
  stars_combo.current(0)
  destruction_entry.delete(0,tk.END)
  trophy_entry.delete(0,tk.END)
  army_entry.delete(0,tk.END)

def clear_detail_entries():
  detail_league_combo.current(0)
  detail_season_entry.delete(0, tk.END)
  detail_date_entry.delete(0,tk.END)
  detail_layout_entry.delete(0,tk.END)
  detail_stars_combo.current(0)
  detail_destruction_entry.delete(0,tk.END)
  detail_trophy_entry.delete(0,tk.END)
  detail_army_entry.delete(0,tk.END)  

#リーグ、リーグ期間をリストに入れる
def rebuild_league_list():
  league_list.clear()

  for defense in defenses:
    found = False

    for league in league_list:
      if league["league"] == defense["league"] and league["season"] == defense["season"]:
        found = True
        break

    if found == False:
      league_list.append({
        "league":defense["league"],
        "season":defense["season"]
      })

#defensesにdefenseの辞書を追加する    リストボックスに表示        csvに保存
def add_defense():
  defense = get_input_data()
  #print(defense)
  if defense is None:
    return
  
  defenses.append(defense)

  rebuild_league_list()
  save_defense()
  update_listbox()
  clear_entries()
  
#検索条件を受けとる
def search_defense():
  search_type = search_type_combo.get()
  search_word = search_entry.get()

  if search_word == "":
    update_listbox()
    return
  
  update_listbox(search_type,search_word)

#リストボックスにリーグ一覧を表示
def update_listbox():
  listbox.delete(0,tk.END)

  for league in league_list:
    text = f"{league['league']} ({league['season']})"
    listbox.insert(tk.END, text)

#リーグ一覧がクリックされたとき
def on_league_selected(event):
  global detail_window
  global detail_listbox
  global summary_listbox
  global detail_league_combo
  global detail_season_entry
  global detail_date_entry
  global detail_layout_entry
  global detail_stars_combo
  global detail_destruction_entry
  global detail_trophy_entry
  global detail_army_entry
  global selected_league

  index = listbox.curselection()

  if not index:
    return
  
  selected_league = league_list[index[0]]

  detail_window = tk.Toplevel(root)
  detail_window.title(f"{selected_league['league']} {selected_league['season']}")
  detail_window.geometry("500x500")

  tk.Label(detail_window,text="集計").pack()
  summary_listbox = tk.Listbox(detail_window)
  summary_listbox.pack()

  army_graph_button = tk.Button(detail_window, text="編成グラフ", command=show_army_graph)
  army_graph_button.pack()

  star_graph_button = tk.Button(detail_window, text="★割合グラフ", command=show_star_graph)
  star_graph_button.pack()

  tk.Label(detail_window, text="防衛データ一覧").pack()
  detail_listbox = tk.Listbox(detail_window, width=70,height=10)
  detail_listbox.pack()

  detail_listbox.bind("<<ListboxSelect>>", on_detail_selected)

  tk.Label(detail_window, text="リーグ").pack()
  detail_league_combo = ttk.Combobox(detail_window, values=["リーグⅠ","リーグⅡ","リーグⅢ"])
  detail_league_combo.pack()

  detail_league_combo.current(0)

  tk.Label(detail_window, text="リーグ期間").pack()
  detail_season_entry = tk.Entry(detail_window)
  detail_season_entry.pack()

  tk.Label(detail_window, text="日付").pack()
  detail_date_entry = tk.Entry(detail_window)
  detail_date_entry.pack()

  tk.Label(detail_window, text="配置ID").pack()
  detail_layout_entry = tk.Entry(detail_window)
  detail_layout_entry.pack()

  tk.Label(detail_window, text="取られた★の数").pack()
  detail_stars_combo = ttk.Combobox(detail_window, values=[0,1,2,3])
  detail_stars_combo.pack()

  detail_stars_combo.current(0)

  tk.Label(detail_window, text="破壊率").pack()
  detail_destruction_entry = tk.Entry(detail_window)
  detail_destruction_entry.pack()
  
  tk.Label(detail_window, text="トロフィー数").pack()
  detail_trophy_entry = tk.Entry(detail_window)
  detail_trophy_entry.pack()

  tk.Label(detail_window, text="編成").pack()
  detail_army_entry = tk.Entry(detail_window)
  detail_army_entry.pack()

  update_button = tk.Button(detail_window, text="更新", command=update_defense)
  update_button.pack()

  delete_button = tk.Button(detail_window ,text="削除", command=delete_defense)
  delete_button.pack()

  update_summary()
  update_detail_listbox()
  
#集計
def update_summary():
  count = 0

  total_stars = 0
  total_destruction = 0
  total_trophy = 0

  army_count = {}
  for defense in defenses:
    if selected_league["league"] == defense["league"] and selected_league["season"] == defense["season"]:
      count += 1
      total_stars += defense["stars"]
      total_destruction += defense["destruction"]
      total_trophy += defense["trophy"]
      army = defense["army"]
      if army in army_count:
        army_count[army] += 1
      else:
        army_count[army] = 1

  if count == 0:
    summary_listbox.delete(0, tk.END)
    return
  
  avg_stars = total_stars / count
  avg_destruction = total_destruction / count
  avg_trophy = total_trophy / count

  summary_listbox.delete(0, tk.END)

  summary_listbox.insert(tk.END, f"防衛回数: {count}回")
  summary_listbox.insert(tk.END, f"平均破壊率: {avg_destruction:.1f}%")
  summary_listbox.insert(tk.END, f"平均★の数: {avg_stars:.2f}")
  summary_listbox.insert(tk.END, f"合計トロフィー: {total_trophy}")
  summary_listbox.insert(tk.END, f"平均トロフィー数: {avg_trophy:.2f}")

  summary_listbox.insert(tk.END, "")
  summary_listbox.insert(tk.END, f"[編成ランキング]")

  ranking = sorted(
    army_count.items(),
    key=lambda x:x[1],
    reverse=True
  )

  for rank, (army, count) in enumerate(ranking, start=1):
    summary_listbox.insert(tk.END, f"{rank}位 {army}: {count}回")


#防衛データ一覧
def update_detail_listbox():
  detail_listbox.delete(0,tk.END)

  detail_indexes.clear()

  num = 0
  for defense in defenses:
    if selected_league["league"] == defense["league"] and selected_league["season"] == defense["season"]:
      text = (
        f"{defense['date']} "
        f"{defense['layout_id']} "
        f"★{defense['stars']} "
        f"{defense['destruction']}% "
        f"{defense['trophy']} "
        f"{defense['army']} "
      )
      detail_indexes.append(num)
      detail_listbox.insert(tk.END,text)
    num += 1

#防衛データ選択後入力欄表示
def on_detail_selected(event):
  index = detail_listbox.curselection()

  if not index:
    return

  global editing_index
  editing_index = detail_indexes[index[0]]        #detail_indexes[]はdefensesの何番目を表示しているかをリストで管理しその数字が入っている
  defense = defenses[editing_index]

  detail_league_combo.set(defense["league"])

  detail_season_entry.delete(0, tk.END)
  detail_season_entry.insert(0, defense["season"])

  detail_date_entry.delete(0, tk.END)
  detail_date_entry.insert(0, defense["date"])

  detail_layout_entry.delete(0, tk.END)
  detail_layout_entry.insert(0, defense["layout_id"])

  detail_stars_combo.set(defense["stars"])

  detail_destruction_entry.delete(0, tk.END)
  detail_destruction_entry.insert(0, defense["destruction"]) 

  detail_trophy_entry.delete(0, tk.END)
  detail_trophy_entry.insert(0, defense["trophy"])

  detail_army_entry.delete(0, tk.END)
  detail_army_entry.insert(0, defense["army"]) 

#編集した後の更新
def update_defense():
  global editing_index

  if editing_index is None:
    messagebox.showwarning("警告", "編集するデータを選択してください")
    return
  
  defense = get_detail_input_data()

  if defense is None:
    return

  defenses[editing_index] = defense

  rebuild_league_list()
  update_summary()
  update_detail_listbox()
  update_listbox()
  save_defense()

  editing_index = None

  messagebox.showinfo("情報", "更新しました")

#削除
def delete_defense():
  global editing_index

  if editing_index is None:
    messagebox.showwarning("警告","削除する項目を選択してください")
    return
  
  answer = messagebox.askyesno("確認","本当に削除しますか？")

  if answer:
    defenses.pop(editing_index)
    rebuild_league_list()

    count = 0

    for defense in defenses:
      if defense["league"] == selected_league["league"] and defense["season"] == selected_league["season"]:
        count += 1

    if count == 0:
      detail_window.destroy()
      update_listbox()
      save_defense()
      editing_index = None
      return
    
    update_summary()
    update_detail_listbox()
    update_listbox()
    save_defense()
    clear_detail_entries()

    editing_index = None

def show_army_graph():
  army_count = {}
  for defense in defenses:
    if selected_league["league"] == defense["league"] and selected_league["season"] == defense["season"]:
      army = defense["army"]
      if army in army_count:
        army_count[army] += 1
      else:
        army_count[army] = 1

  labels = list(army_count.keys())
  values = list(army_count.values())

  plt.rcParams["font.family"] = "Yu Gothic"

  plt.figure(figsize=(5, 5))

  plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)

  plt.title("編成割合")

  plt.show()

def show_star_graph():
  stars_count = {}

  for defense in defenses:
    if selected_league["league"] == defense["league"] and selected_league["season"] == defense["season"]:
      stars = defense["stars"]
      if stars in stars_count:
        stars_count[stars] += 1
      else:
        stars_count[stars] = 1

  labels = [f"★{star}" for star in stars_count.keys()]
  values = list(stars_count.values())

  plt.rcParams["font.family"] = "Yu Gothic"

  plt.figure(figsize=(5, 5))

  plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)

  plt.title("★割合")

  plt.show()

#csvに保存
def save_defense():
  with open("defenses.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["リーグ","リーグ期間","日付","配置ID","★の数","破壊率","トロフィー数","編成"])

    for defense in defenses:
      writer.writerow([
        defense['league'],
        defense['season'],
        defense['date'],
        defense['layout_id'],
        defense['stars'],
        defense['destruction'],
        defense['trophy'],
        defense['army']
      ])

    #messagebox.showinfo("情報","csvファイルに保存しました")

#csvの読み込み
def load_defense():
  try:
    with open("defenses.csv", "r", encoding="utf-8-sig") as file:
      reader = csv.reader(file)

      next(reader)

      for row in reader:
        defense = {
          "league":row[0],
          "season":row[1],
          "date":row[2],
          "layout_id":row[3],
          "stars":int(row[4]),
          "destruction":int(row[5]),
          "trophy":int(row[6]),
          "army":row[7]
        }

        defenses.append(defense)
      rebuild_league_list()
  except FileNotFoundError:
    pass

root = tk.Tk()

root.title("クラクラ 防衛戦績")
root.geometry("500x400")

tk.Label(root, text="クラクラ 防衛戦績").pack()

tk.Label(root, text="リーグ").pack()

#リーグ選択欄
league_combo = ttk.Combobox(root, values=["リーグⅠ","リーグⅡ","リーグⅢ"])
league_combo.pack()

league_combo.current(0)

#リーグ期間の入力
tk.Label(root, text="リーグ期間").pack()

season_entry = tk.Entry(root)
season_entry.pack()

#日付入力欄
tk.Label(root, text="日付").pack()

date_entry = tk.Entry(root)
date_entry.pack()

#配置入力欄
tk.Label(root, text="配置ID").pack()

layout_entry = tk.Entry(root)
layout_entry.pack()

#★の数選択欄
tk.Label(root, text="取られた★の数").pack()

stars_combo = ttk.Combobox(root, values=[0,1,2,3])
stars_combo.pack()

stars_combo.current(0)

#破壊率入力欄
tk.Label(root, text="破壊率").pack()

destruction_entry = tk.Entry(root)
destruction_entry.pack()

#トロフィー数入力欄
tk.Label(root, text="トロフィー数").pack()

trophy_entry = tk.Entry(root)
trophy_entry.pack()

#編成入力欄
tk.Label(root, text="編成").pack()

army_entry = tk.Entry(root)
army_entry.pack()

#追加ボタン
add_button = tk.Button(root, text="追加", command=add_defense)
add_button.pack()

#リーグとリーグ期間一覧
listbox = tk.Listbox(root)
listbox.pack()

listbox.bind("<<ListboxSelect>>", on_league_selected)

load_defense()
update_listbox()

root.mainloop()