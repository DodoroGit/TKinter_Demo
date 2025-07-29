import tkinter as tk
import ttkbootstrap as tkbs
import psycopg2
import openai
import threading
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class RootWindow() :
    def __init__( self, root ) :
        self.root = root
        root.title( "GPT測試介面" )
        root.geometry( "800x600" )
        root.resizable( True, True )
        root.iconbitmap( "GPT.ico" )
        self.photo = tk.PhotoImage( file="images.png" )
        label = tk.Label(root, justify=tk.LEFT, image=self.photo, compound=tk.CENTER, font=("Arial", 20), fg="white")
        label.pack( pady = 10 )
        turn_mainpage = MainPage( self.root )

class MainPage() :
    def __init__( self, root ) :
        self.root = root
        self.account = tk.StringVar()
        self.password = tk.StringVar()
        self.msg = tk.StringVar()
        
        self.frame1 = tk.Frame( self.root )
        self.frame1.pack() 

        self.UserName_label = tk.Label( self.frame1, text="請輸入帳號 : ", font = "標楷體" )
        self.UserName_label.grid( row = 0, column = 0)
        self.Password_label = tk.Label( self.frame1, text="請輸入密碼 : ", font = "標楷體" )
        self.Password_label.grid( row = 1, column = 0 )

        self.UserName_entry = tk.Entry( self.frame1, textvariable = self.account, font = "Arial" )
        self.UserName_entry.grid(row = 0, column = 1)
        self.Password_entry = tk.Entry( self.frame1, textvariable = self.password, font ="Arial", show = '*' )
        self.Password_entry.grid( row = 1, column = 1, pady = 5 )
        
        self.Login_button = tk.Button( self.frame1, text="登入", command = self.CheckPassword, font= "標楷體" )
        self.Login_button.grid( row = 2, column = 1 )

        self.respones = tk.Label( self.frame1, textvariable = self.msg, font = "標楷體" )  
        self.respones.grid(row = 3, column = 1 )

    def CheckPassword( self ) :
        if ( self.account.get() == "" and self.password.get() == "" ) :
            self.msg.set("歡迎登入本系統")
            self.frame1.destroy()
            self.turn_secondpage = SecondPage( self.root ) 
        else :
            self.msg.set("帳號或密碼錯誤，請修正後重新登入 !") 

class SecondPage() :
    def __init__( self, root ) :
        self.root = root
        self.messages_save  = tk.StringVar()
        self.messages_input = tk.StringVar()
        self.frame2 = tk.Frame( self.root )
        self.frame2.pack()

        self.function_one   = tk.Button( self.frame2, text = "功能一 : 詢問模型問題", font = "標楷體", command = self.Function1 ) 
        self.function_two   = tk.Button( self.frame2, text = "功能二 : 輸入資料進入系統", font = "標楷體", command = self.Function2 )  
        self.function_three = tk.Button( self.frame2, text = "功能三 : 詢問更新過資料的模型問題", font = "標楷體", command = self.Function3 ) 
        self.function_four  = tk.Button( self.frame2, text = "功能四 : 回到登入畫面", font = "標楷體", command = self.Function4 ) 
        
        self.function_one.grid( row = 0, column = 0, pady = 10 )
        self.function_two.grid( row = 1, column = 0, pady = 10  ) 
        self.function_three.grid( row = 2, column = 0, pady = 10  ) 
        self.function_four.grid( row = 3, column = 0, pady = 10  ) 

    def Function1( self ) :
        self.frame2.destroy()
        self.frame3 = tk.Frame( self.root )
        self.frame3.pack()

        Question_label = tk.Label( self.frame3, text="請輸入想要詢問的問題 : ", font = "標楷體" )
        Question_label.grid( row = 0, column = 0)

        Question_entry = tk.Entry( self.frame3, textvariable = self.messages_input, font = "標楷體", width=40  )
        Question_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        Question_button = tk.Button( self.frame3, text = "輸入", font = "標楷體", command = self.start_question1_thread )
        Question_button.grid(row = 0, column = 2 )
        
        back_button = tk.Button( self.frame3, text = "返回功能列表", font = "標楷體", command = self.F1back )
        back_button.grid( row = 1 , column = 1) 

    def Function2( self ) :
        self.frame2.destroy()
        self.frame4 = tk.Frame( self.root )
        self.frame4.pack()
        
        input_label = tk.Label( self.frame4, text="請輸入想要輸入的資訊 : ", font = "標楷體" )
        input_label.grid( row = 0, column = 0)

        input_entry = tk.Entry( self.frame4, textvariable = self.messages_input, font = "標楷體", width=40 )
        input_entry.grid( row = 0, column = 1, pady = 10 )
        
        input_button = tk.Button( self.frame4, text = "輸入", font = "標楷體", command = self.question2 )
        input_button.grid( row = 0, column = 2, padx = 10 )
        
        back_button = tk.Button( self.frame4, text = "返回功能列表", font = "標楷體", command = self.F2back)
        back_button.grid( row = 1, column = 1, pady = 10 )

        query_button = tk.Button( self.frame4, text = "查詢目前輸入的資料", font = "標楷體", command = self.Query)
        query_button.grid( row = 2, column = 1)

    def Function3( self ) :
        self.frame2.destroy()
        self.frame5 = tk.Frame()
        self.frame5.pack()
        
        Question_label = tk.Label( self.frame5, text="請輸入想要詢問的問題 : ", font = "標楷體" )
        Question_label.grid( row = 0, column = 0)

        Question_entry = tk.Entry( self.frame5, textvariable = self.messages_input, font = "標楷體", width = 40  )
        Question_entry.grid( row = 0, column = 1, padx = 10, pady = 10 )
        
        Question_button = tk.Button( self.frame5, text = "輸入", font = "標楷體", command = self.start_question3_thread )
        Question_button.grid( row = 0, column = 2 )
        
        back_button = tk.Button( self.frame5, text = "返回功能列表", font = "標楷體", command = self.F3back )
        back_button.grid( row = 1 , column =1)

    def Function4 (self ) :
        self.frame2.destroy()
        TurnMainPage = MainPage( self.root ) 

    def question1( self ) :
        self.frame3.destroy()
        self.frame6 = tk.Frame( root )
        self.frame6.pack()
        
        prompt = self.messages_input.get() 
        print( prompt )

        messages = []
        messages.append({"role":"user","content":prompt})   # 添加 user 回應
        
        try : 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=256,
                temperature=0.5,
                messages=messages,
            )
        except Exception as exc :
            print(exc)
        
        print( response.choices[0].message.content.replace('\n','') )
        
        
        answer_label = tk.Label( self.frame6, text=response.choices[0].message.content.replace('\n',''), font = "標楷體",  wraplength = 600 )
        answer_label.grid( row = 1, column = 1 )
        
        back_button = tk.Button( self.frame6, text = "返回功能列表", font = "標楷體", command = self.Q1back )
        back_button.grid( row = 2 , column = 1)

    def question2( self ) :
        self.frame4.destroy()
        self.frame8 = tk.Frame( self.root ) 
        self.frame8.pack()
        try:
            cursor.execute( "insert into gui ( data_save ) values ( '{}' )".format( self.messages_input.get() ) )
            conn.commit() 
            input_label = tk.Label( self.frame8, text="成功輸入資料進入資料庫", font = "標楷體" )
            input_label.grid( row = 0, column = 0)
        except :
            print( "輸入資料庫錯誤!" )

        back_button = tk.Button( self.frame8, text = "返回功能列表", font = "標楷體", command = self.Q2back )
        back_button.grid( row = 1, column = 0)
        
    def question3( self ) :
        self.frame5.destroy()
        self.frame7 = tk.Frame( self.root )
        self.frame7.pack()
        
        cursor.execute( "select data_save from gui" )
        data = cursor.fetchall()
        cursor.execute( "SELECT COUNT(*) FROM gui" )
        record_count = cursor.fetchone()[0]

        prompt = ""
        print( record_count )
        for i in range( record_count ) :
            prompt = prompt + data[i][0] + "\n"
        
        prompt = prompt + self.messages_input.get() + "\n"
        print( prompt ) 

        messages = []
        messages.append({"role":"user","content": prompt} )   # 添加 user 回應
        
        try : 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=256,
                temperature=0.5,
                messages=messages
            )
        except Exception as exc :
            print(exc)
        
        print( response.choices[0].message.content.replace('\n','') )
        
        answer_label = tk.Label( self.frame7, text=response.choices[0].message.content.replace('\n',''), font = "標楷體",  wraplength = 600 )
        answer_label.grid( row = 1, column = 1 )
        
        back_button = tk.Button( self.frame7, text = "返回功能列表", font = "標楷體", command = self.Q3back )
        back_button.grid( row = 2 , column = 1)

    def F1back( self ) :
        self.frame3.destroy() 
        TurnSecondPage = SecondPage( self.root ) 

    def F2back( self ) :
        self.frame4.destroy()
        TurnSecondPage = SecondPage( self.root )

    def F3back( self ) :
        self.frame5.destroy()
        TurnSecondPage = SecondPage( self.root )

    def Q1back( self ) :
        self.frame6.destroy() 
        TurnSecondPage = SecondPage( self.root ) 

    def Q2back( self ) :
        self.frame8.destroy()
        TurnSecondPage = SecondPage( self.root )

    def Q3back( self ) :
        self.frame7.destroy()
        TurnSecondPage = SecondPage( self.root )

    def start_question3_thread( self ):
        # 使用多執行緒處理 question3 方法
        thread = threading.Thread( target = self.question3 )
        thread.start()

    def start_question1_thread( self ):
        # 使用多執行緒處理 question1 方法
        thread = threading.Thread( target = self.question1 )
        thread.start()

    def Query( self ) :
        self.frame4.destroy()
        self.frame9 = tk.Frame( self.root )
        self.frame9.pack()

        cursor.execute( "select data_save from gui" )
        data = cursor.fetchall()
        cursor.execute( "SELECT COUNT(*) FROM gui" )
        record_count = cursor.fetchone()[0]

        prompt = ""
        print( record_count )
        for i in range( record_count ) :
            prompt = prompt + data[i][0] + "\n"

        data_label = tk.Label( self.frame9, text = prompt, font = "標楷體", width = 60 )
        data_label.grid( row = 0, column = 0)

        back_button = tk.Button( self.frame9, text = "返回功能列表", font = "標楷體", command = self.QueryBack )
        back_button.grid( row = 1, column = 0)

    def QueryBack( self ) :
        self.frame9.destroy()
        SecondPage( self.root )


if __name__ == "__main__" :

    conn = psycopg2.connect( dbname = "postgres", user = "postgres", password = "871218", host = "localhost", port = "5432" )
    cursor = conn.cursor()
    sql = "create table if not exists gui( id serial PRIMARY KEY, data_save VARCHAR(5000)) ;" 
    cursor.execute( sql)
    conn.commit()

    root = tk.Tk()
    style = tkbs.Style( theme = "morph" )
    app = RootWindow( root ) 
    root.mainloop()