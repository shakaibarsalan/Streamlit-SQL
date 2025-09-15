

# Talk to Your Database (Prompt-to-SQL with LangChain & Streamlit)

This project allows you to **interact with a MySQL database** using natural language queries.  
You can upload a `.sql` file, the app will create/load the database, and then you can ask questions in plain English.  
The system uses **LangChain + Google Gemini models** to generate SQL queries automatically and display results.

---

## 🚀 Features
- Upload `.sql` file → auto-detect database name & initialize tables.  
- Choose Google Gemini model (`gemini-2.5-flash`, `gemini-1.5-flash`).  
- Enter natural language queries → get **valid SQL queries**.  
- Execute queries on the MySQL database & view results in a table.  

---

## 📂 Project Structure
```

project-root/
│── myapp3.py              # Main Streamlit application
│── requirements.txt       # Python dependencies
│── .env                   # Environment variables (GOOGLE\_API\_KEY)

````

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
````

### 2. Create Conda Environment

```bash
conda create -n env_langchain1 python=3.10
conda activate env_langchain1
```

### 3. Go to Project Directory

```bash
d:
cd "prompt to sql text"
cd talk-to-DB
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Setup Environment Variables

Create a `.env` file in the project root with:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 6. Run the Streamlit App

```bash
streamlit run myapp3.py
```

---

## 🗄️ Requirements

* **Python 3.10+**
* **MySQL** installed & running locally (`root/root123` by default in the code).
* A `.sql` file to upload.
* Google API Key for Gemini models.

---

## 🔑 Example Usage

1. Run the app.
2. Upload your `.sql` file (with `CREATE DATABASE` or `USE` statement).
3. Ask a question like:

   ```
   Show me all customers who placed orders in the last 30 days
   ```
4. The app will:

   * Generate SQL query.
   * Execute it on the database.
   * Show query + results in a nice table.

---

## 🛠️ Tech Stack

* **Python** (3.10)
* **Streamlit** (UI)
* **LangChain** (LLM orchestration)
* **Google Gemini** (LLM)
* **SQLAlchemy** (DB connection)
* **MySQL + PyMySQL**


