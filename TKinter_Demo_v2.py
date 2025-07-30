import tkinter as tk
import ttkbootstrap as tkbs
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
        root.iconbitmap( "image/num1.ico" )
        self.photo = tk.PhotoImage( file="image//test2.png" )
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
        self.function_two   = tk.Button( self.frame2, text = "功能二 : 檢查匯入資料", font = "標楷體", command = self.Function3 ) 
        self.function_four  = tk.Button( self.frame2, text = "功能三 : 回到登入畫面", font = "標楷體", command = self.Function2 ) 
        
        self.function_one.grid( row = 0, column = 0, pady = 10 )
        self.function_two.grid( row = 1, column = 0, pady = 10 )
        self.function_four.grid( row = 2, column = 0, pady = 10  ) 

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

    def Function2 ( self ) :
        self.frame2.destroy()
        TurnMainPage = MainPage( self.root ) 

    def Function3 ( self ) :
        self.frame2.destroy()
        self.frame4 = tk.Frame( self.root )
        self.frame4.pack()

        
        file = open( "prompt.txt", "r", encoding='utf-8' )
        title_label = tk.Label( self.frame4, text = "文字檔內容", font=("標楷體", 20))
        title_label.grid( row = 1, column = 0 )
        
        scrollbar = tk.Scrollbar( self.frame4 )
        scrollbar.grid( row =2, column = 1, sticky='ns' )

        # 創建文本區域
        text_area = tk.Text( self.frame4, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=20, width=50)
        text_area.grid( row = 2, column = 0 )

        # 將滾動條與文本區域連接
        scrollbar.config( command=text_area.yview)

        # 插入大量文本
        text_area.insert( tk.END, file.read() )
        file.close()

        back_button = tk.Button( self.frame4, text = "返回功能列表", font = "標楷體", command = self.Q1back )
        back_button.grid( row = 3, column = 0 )




    def question1( self ) :

        self.frame3.destroy()
        self.frame4 = tk.Frame( self.root )
        self.frame4.pack()

        prompt = ""

        try :
            file = open( "prompt.txt", "r", encoding='utf-8' )
            print ( file.read() )
        except :
            prompt = ""
        
        file.close()
        print( prompt )

        prompt = prompt + self.messages_input.get() + "\n"
        messages = []
        messages.append( {"role":"user","content": "幫我用200字以內簡短回答"} )
        messages.append( {"role":"user","content": prompt} )   # 添加 user 回應

        print( "messages", messages )
        
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=1,
            max_tokens=350,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print( response.choices[0].message.content.strip() )
        
        answer_label = tk.Label( self.frame4, text=response.choices[0].message.content.replace('\n',''), font = "標楷體",  wraplength = 600 )
        answer_label.grid( row = 1, column = 1 )
        
        back_button = tk.Button( self.frame4, text = "返回功能列表", font = "標楷體", command = self.Q1back )
        back_button.grid( row = 2 , column = 1)
    

    def F1back( self ) :
        self.frame3.destroy() 
        TurnSecondPage = SecondPage( self.root ) 

    def Q1back( self ) :
        self.frame4.destroy()
        TurnSecondPage = SecondPage( self.root )


    def start_question1_thread( self ):
        # 使用多執行緒處理 question1 方法
        thread = threading.Thread( target = self.question1 )
        thread.start()


if __name__ == "__main__" :

    root = tk.Tk()
    style = tkbs.Style( theme = "morph" )
    app = RootWindow( root ) 
    root.mainloop()