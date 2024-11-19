import lib
lib.connect_db()
while True:  
     #while true:
     print("\n--- 電影管理系統 ---")
     print("1. 匯入電影資料檔\n2. 查詢電影\n3. 新增電影\n4. 修改電影\n5. 刪除電影\n6. 匯出電影\n7. 離開系統")
     print("------------------------")  
     choice = input("請選擇操作選項 (1-7):  ")
     if(choice=='1'):
          lib.import_movies()
     elif(choice=='2'):
         lib.search_movies()
     elif(choice=='3'):
         lib.add_movie()
     elif(choice=='4'):
         lib.modify_movie()
     elif(choice=='5'):
         lib.delete_movies()
     elif(choice=='6'):
         lib.export_movies() 
     elif (choice == '7'):
         lib.off()
         break # 退出選項
     else:
         print("無效的選項，請重新選擇。") 
        

