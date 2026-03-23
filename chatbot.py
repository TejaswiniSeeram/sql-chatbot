import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
DB_PATH = "data/chinook.db"

# Get all the table names and column names for each table and return it to the LLM
def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    schema = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for  table in tables:
        table_name = table[0]
        schema += f"Table: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = ", ".join([column[1] for column in columns]) 
        schema += f"Columns: {column_names}\n\n"
    conn.close()
    return schema


#Send schema + question to LLM, get SQL query back
def generate_sql(question, schema):
    prompt = f"""
    You are a SQL expert. Here is the database schema: {schema}
    Write a SQLite SQL query for this question: {question}
    Return ONLY the SQL query, nothing else
    No markdown, no backticks, no explanation
    """
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0
    )
    return response.choices[0].message.content.strip()

#Run the SQL query on the database
def run_sql(sql_query):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        column_names = [desc[0] for desc in cursor.description]        
        rows=cursor.fetchall()
        conn.close()
        return column_names,rows
    except Exception as e:
        return None, str(e)


#Send results to LLM, get plain English answer
def generate_answer(question, sql_query, columns, rows):
    prompt = f"""
    Explain the results in plain English and Be concise and friendly
    The user asked: {question}
    This SQL was run: {sql_query}
    These are the results: {rows}
    These are the column names: {columns}
    """
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
    

def sql_chain(question):
    schema = get_schema()
    sql_query = generate_sql(question, schema)
    columns, rows = run_sql(sql_query)
    if columns is None:
        return rows, sql_query  # rows holds the error message here
    answer = generate_answer(question, sql_query, columns, rows)
    return answer, sql_query

if __name__ == "__main__":
    answer, sql = sql_chain("How many artists are in the database?")
    print("SQL:", sql)
    print("Answer:", answer)