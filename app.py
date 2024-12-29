import sqlite3
import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key="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"  # Replace with your actual OpenAI API key
)

# Database setup
def setup_database(db_name="faq_system.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to log query and response
def log_to_database(question, response, db_name="faq_system.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO logs (question, response, timestamp)
        VALUES (?, ?, ?)
    ''', (question, response, timestamp))
    conn.commit()
    conn.close()


def get_response_from_chatgpt(question):
    prompt = f"You are a support assistant. Answer the following question in one paragraph: {question}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content 


def run_faq_system():
    print("Automated FAQ System. Type 'exit' to quit.")
    while True:
        question = input("Enter your question: ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        try:
            response = get_response_from_chatgpt(question)
            log_to_database(question, response)
            print("Response:", response)
        except Exception as e:
            print("Error:", e)


setup_database()
run_faq_system()
