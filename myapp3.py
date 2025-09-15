import os
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import pandas as pd  # Added for DataFrame support

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ----------------- Load environment variables -----------------
load_dotenv()

# ----------------- Streamlit UI -----------------
st.title("Talk to Your MySQL Database via Uploaded SQL File 🗄️")

# MySQL connection parameters
db_user = "root"
db_password = "root123"
db_host = "localhost"

uploaded_file = st.file_uploader("Upload your SQL file", type=["sql"])

engine = None
db = None

if uploaded_file:
    try:
        # Read SQL file
        sql_script = uploaded_file.read().decode("utf-8")

        # Step 1: Detect database name
        db_name = None
        for line in sql_script.splitlines():
            if line.strip().upper().startswith("USE "):
                db_name = line.strip().split()[1].replace(";", "")
                break
            if line.strip().upper().startswith("CREATE DATABASE"):
                parts = line.strip().split()
                if len(parts) >= 3:
                    db_name = parts[2].replace(";", "")
        
        if not db_name:
            st.error("Could not detect database name from SQL file (missing USE or CREATE DATABASE).")
        else:
            # Step 2: Connect without DB, create database if not exists
            temp_engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}")
            with temp_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))

            # Step 3: Connect directly to that DB
            engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
            with engine.connect() as conn:
                # Remove CREATE DATABASE/USE lines before executing
                cleaned_sql = []
                for line in sql_script.splitlines():
                    if line.strip().upper().startswith("CREATE DATABASE"):
                        continue
                    if line.strip().upper().startswith("USE "):
                        continue
                    cleaned_sql.append(line)
                cleaned_sql = "\n".join(cleaned_sql)

                # Execute remaining SQL
                for statement in cleaned_sql.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        try:
                            conn.execute(text(stmt))
                        except Exception as e:
                            st.warning(f"Skipped statement: {stmt[:50]}... ({e})")

            # Step 4: Initialize SQLDatabase for LLM
            db = SQLDatabase(engine, sample_rows_in_table_info=0)
            st.success(f"✅ SQL file executed and connected to `{db_name}` successfully!")

    except Exception as e:
        st.error(f"Error loading SQL file: {e}")

# ----------------- Step 2: Initialize LLM -----------------
model_choice = st.selectbox(
    "Select Gemini model:",
    ["gemini-2.5-flash", "gemini-1.5-flash"],
    index=0
)

llm = ChatGoogleGenerativeAI(
    model=model_choice,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

# ----------------- Step 3: Prompt Template -----------------
sql_prompt = PromptTemplate(
    input_variables=["input", "table_info"],
    template="""
You are a MySQL expert.
Given the database schema below:

{table_info}

Write a valid SQL query for the following request:
{input}

⚠️ Rules:
- Only return the SQL query (no explanations, no SQLQuery: prefix, no markdown fences).
- Do NOT add LIMIT unless the user explicitly asks for it.
    """
)

custom_chain = LLMChain(llm=llm, prompt=sql_prompt)

# ----------------- Step 4: Query Execution -----------------
def execute_query(question):
    try:
        generated_query = custom_chain.run({
            "input": question,
            "table_info": db.table_info
        })

        query_str = str(generated_query).strip()

        # Execute query and fetch results as a DataFrame
        with engine.connect() as conn:
            df = pd.read_sql(query_str, conn)
        
        return query_str, df

    except ProgrammingError as e:
        st.error(f"⚠️ SQL execution error: {e}")
        return None, None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None, None

# ----------------- Step 5: Ask Prompt -----------------
if db:
    question = st.text_input("Enter your question about the uploaded database:")

    if st.button("Execute"):
        if question:
            cleaned_query, query_result = execute_query(question)

            if cleaned_query and query_result is not None:
                st.write("### Generated SQL Query")
                st.code(cleaned_query, language="sql")

                # st.write("### Query Result (Raw)")
                # st.write(query_result.to_string())  # Display raw result as before

                st.write("### Query Result (Table)")
                st.dataframe(query_result)  # Display result as a table
            else:
                st.info("No result returned due to an error.")
        else:
            st.warning("Please enter a question.")
else:
    st.info("👆 Please upload a `.sql` file first.")