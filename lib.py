import sqlite3
import os
import json
from pprint import PrettyPrinter

JSON_IN_PATH = 'movie.json'
DB_PATH= 'movie.db'
JSON_OUT_PATH='exported.json'

conn = sqlite3.connect('movie.db')  # 連線資料庫
conn.row_factory = sqlite3.Row # 設置 row_factory
cursor = conn.cursor()  # 建立 cursor 物件


def connect_db():
    try:
       conn.execute('''CREATE TABLE IF NOT EXISTS movie("id"	INTEGER,
	"title"	TEXT NOT NULL,
	"director"	TEXT NOT NULL,
	"genre"	TEXT NOT NULL,
	"year"	INTEGER NOT NULL,
	"rating"	REAL NOT NULL CHECK("rating" >= 1.0 AND "rating" <= 10.0),
	PRIMARY KEY("id" AUTOINCREMENT))''')
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")
    except Exception as e:
        print(f'發生其它錯誤 {e}')

def  import_movies():    # 將 JSON 資料插入到資料庫
    with open(JSON_IN_PATH, "r", encoding="utf-8") as file:
        movies = json.load(file)
    for movie in movies:
        cursor.execute('INSERT INTO "movie" (title, director, genre, year, rating) VALUES (?, ?, ?, ?, ?)',(movie["title"], movie["director"], movie["genre"], movie["year"], movie["rating"]))  # 参数应为元组或列表
    conn.commit()
    print("資料已成功匯入資料庫！")


def search_movies():
    f = input("查詢全部電影嗎？(y/n): ").strip().lower()

    if f == 'y': 
        cursor.execute('SELECT * FROM movie')
        result_all = cursor.fetchall()

        if not result_all:  # 如果沒有資料
            print("查無資料")
            return  # 結束函式

        print("\n")
        print(f"{'電影名稱':{chr(12288)}<10}{'導演':<10}{'  類型':>10}{'上映年份':>12}{'評分':>11}")
        print("------------------------------------------------------------------------")

        for row in result_all:
            print(f"{row[1]:{chr(12288)}<10}{row[2]:{chr(12288)}<10}{row[3]:<10}{row[4]:<12}{row[5]:>11}")

    else: 
        title = input("請輸入電影名稱: ").strip()
        cursor.execute("SELECT * FROM movie WHERE title LIKE ?", (f'%{title}%',))
        result_single = cursor.fetchone()  # 獲取第一筆匹配資料

        if not result_single:  # 如果找不到資料
            print(f"找不到名稱包含「{title}」的電影。")
            return  # 結束函式

        print("\n")
        print(f"{'電影名稱':{chr(12288)}<10}{'導演':<10}{'  類型':>10}{'上映年份':>12}{'評分':>11}")
        print("------------------------------------------------------------------------")
        print(f"{result_single[1]:{chr(12288)}<10}{result_single[2]:{chr(12288)}<10}{result_single[3]:<10}{result_single[4]:<12}{result_single[5]:<10.2}")



# 新增
def add_movie():
    cursor.execute('SELECT MAX(id) FROM "movie"')


    # 輸入電影資料
    title = input("電影名稱: ")
    director = input("導演: ")
    genre = input("類型: ")
    year = input("上映年份: ")
    rating = input("評分(1.0 - 10.0): ")

    
    # 插入其他資料到各自的表格
    cursor.execute('INSERT INTO "movie" (title,director,genre,year,rating) VALUES (?,?,?,?,?)', (title,director,genre,year,rating))

    # 提交更改
    conn.commit()
    print("電影已新增")

# 修改資料
def modify_movie():
    # 從每個表格中提取資料
    cursor.execute('SELECT * FROM "movie"')

    change = input("請輸入要修改的電影名稱: ")
    cursor.execute("SELECT * FROM movie WHERE title like ?", (f'%{change}%',))
    row=cursor.fetchone()
    print("\n")
    print(f"{'電影名稱':{chr(12288)}<10}{'導演':<10}{'  類型':>10}{'上映年份':>12}{'評分':>11}")
    print("------------------------------------------------------------------------")
    # 顯示當前資料
    print(f"{row[1]:{chr(12288)}<10}{row[2]:{chr(12288)}<10}{row[3]:<10}{row[4]:<12}{row[5]:>11}")

     # 使用者輸入新資料或按 Enter 保持原值
    change_title = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ")
    if change_title == "":
        change_title = row[1]  # 若使用者按 Enter，保持原名稱不變

    change_director = input("請輸入新的導演 (若不修改請直接按 Enter): ")
    if change_director == "":
        change_director =row[2]

    change_genre = input("請輸入新的類型 (若不修改請直接按 Enter): ")
    if change_genre == "":
        change_genre = row[3]

    change_year = input("請輸入新的上映年份 (若不修改請直接按 Enter): ")
    if change_year == "":
        change_year = row[4]

    change_rating = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ")
    if change_rating == "":
        change_rating = row[5]

    cursor.execute('UPDATE movie SET title = ?, director = ?, genre = ?, year = ?, rating = ? WHERE title = ?', (change_title, change_director, change_genre, int(change_year), float(change_rating), change))
    conn.commit()
    print("資料已修改")


# 刪除資料
def delete_movies():
    a = input("刪除全部電影嗎？(y/n): ")

    if a == 'y':
        # 刪除所有資料
        cursor.execute('DELETE FROM "movie";')
        conn.commit()
        print("全部電影已刪除")
    elif a == 'n':
        b = input("請輸入要刪除的電影名稱: ")
        
        # 查找是否存在該電影
        cursor.execute('SELECT * FROM "movie" WHERE title LIKE ?', (f"%{b}%",))
        movies = cursor.fetchall()

        if not movies:
            print("查無此電影")
            return

        # 打印找到的電影信息
        print(f"{'電影名稱':{chr(12288)}<10}{'導演':<10}{'類型':<10}{'上映年份':<10}{'評分':<10}")
        print("------------------------------------------------------------------------")
        for row in movies:
            print(f"{row[1]:{chr(12288)}<10}{row[2]:<10}{row[3]:<10}{row[4]:<10}{row[5]:<10}")

        confirm = input(f"確定要刪除此電影嗎？(y/n): ")
        if confirm == 'y':
            cursor.execute('DELETE FROM "movie" WHERE title LIKE ?', (f"%{b}%",))
            conn.commit()
            print(f" 電影已刪除")
        else:
            print("操作已取消")
    else:
        print("無效輸入，請重新選擇")



def export_movies():
    p=input("匯出全部電影嗎？(y/n): ")

    if(p=='y'):
        # 匯出全部資料
        cursor.execute('SELECT * FROM "movie"')
        conn.row_factory = sqlite3.Row 
        movies = cursor.fetchall()

        # 將資料ㄈ寫入 JSON 檔案
        with open('exported.json', 'w', encoding="utf-8") as f:
            json.dump([dict(row) for row in movies], f, ensure_ascii=False, indent=4)
        print("電影資料已匯出至 exported.json")


    
    else:
        # 匯出單一電影
        title = input("請輸入要匯出的電影名稱: ")
        cursor.execute('SELECT * FROM "movie" WHERE title LIKE ?', (f'%{title}%',))
        movie_data = cursor.fetchone()

        if movie_data:
            # 獲取欄位名稱並結構化單筆資料
            with open('exported.json', 'w', encoding="utf-8") as f:
                json.dump(dict(movie_data), f, ensure_ascii=False, indent=4)
            print("電影資料已匯出至 exported.json")
        else:
            print(f"找不到名稱包含「{title}」的電影。")
def off():
    print("系統已退出")
    cursor.close
    conn.close
    