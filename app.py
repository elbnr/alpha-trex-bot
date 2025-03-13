from flask import Flask, render_template, request
import mysql.connector
import openai

app = Flask(__name__)

# OpenAI API Key
openai.api_key = "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"

# Database Credentials
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "00008888"
DB_NAME = "botman"

# Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Function to generate SQL query using OpenAI
def generate_sql_query(user_question):
    prompt = f"""
    You are a MySQL expert. Convert the following user query into an SQL statement:
    - Database table: sales
    - Columns: id, sale_date, sales, product, region

    User Query: "{user_question}"
    SQL Query:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    sql_query = response['choices'][0]['message']['content'].strip()
    return sql_query

# Function to execute SQL query
def execute_sql_query(sql_query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result if result else "No data found."
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}"

# Function to get bot response
def get_bot_response(user_input):
    sql_query = generate_sql_query(user_input)
    data = execute_sql_query(sql_query)
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["query"]
        response = get_bot_response(user_input)
        return render_template("index.html", response=response)
    return render_template("index.html", response=None)

if __name__ == '__main__':
    app.run(debug=True)
