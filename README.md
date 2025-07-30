# 🎨 TKinter GPT 應用程式 Demo

本專案是一個以 Python `Tkinter` 為基礎的桌面應用程式，搭配 OpenAI GPT 模型，提供簡易介面讓使用者登入後，進行多種文字互動功能。本專案目前包含兩個版本，並搭配 `ttkbootstrap` 提供美化視覺效果。

---

## 🧠 專案特色

- 🔐 登入驗證流程（無帳密要求）
- 🤖 串接 OpenAI GPT-3.5 / GPT-4 API，提供模型互動
- 💾 PostgreSQL 資料儲存（v1）
- 📄 載入本地文字檔（v2）
- 🧪 支援多執行緒處理，避免 UI 卡頓

---

## 📁 專案結構

```
├── TKinter_Demo_v1.py # v1：含資料庫互動與三項功能選單
├── TKinter_Demo_v2.py # v2：簡化流程，載入 prompt.txt 檔案進行問答
├── prompt.txt # 測試文本，供 GPT 使用
├── TKinter_GPT_v2.exe # 編譯後可執行檔（v2）
└── image/
├── num1.ico # 視窗圖示
└── test2.png # GUI 標題圖片
```


---

## 🚀 執行方式

### 1. 安裝套件

```bash
pip install openai psycopg2 ttkbootstrap
```

### 2. 設定 OpenAI API 金鑰
```
export OPENAI_API_KEY=your_api_key

or 

openai.api_key = "your_api_key"
```

### 3. 執行程式
```
python TKinter_Demo_v1.py

python TKinter_Demo_v2.py
```

## 🧪 功能介紹

v1 版本（TKinter_Demo_v1.py）
功能一： 問 GPT 模型問題

功能二： 將輸入資料寫入 PostgreSQL

功能三： 查詢資料庫內容後，結合新輸入再次詢問 GPT


v2 版本（TKinter_Demo_v2.py）
功能一： 問 GPT 模型問題

功能二： 載入 prompt.txt 文字檔作為參考資訊，並回答問題

功能三： 返回登入畫面

## 📌 備註
v1 使用 PostgreSQL，需先啟動本地資料庫並建立 gui 表。

v2 使用本地檔案 prompt.txt 作為語境輸入，不需資料庫。

兩版本皆支援 GPT 多執行緒呼叫，避免主執行緒阻塞。

## 🛠 編譯為 EXE（可選）

```
pip install pyinstaller
pyinstaller --onefile --noconsole TKinter_Demo_v2.py
```

