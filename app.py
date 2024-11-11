import os
import psycopg2
import ollama
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)


# Function to connect to local TimescaleDB
def connect_db():
    try:
        database_url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


# Get related story fragmen
def get_story_fragment(user_query):
    conn = connect_db()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
            SELECT id, fragment, embedding
            FROM story_embeddings
            ORDER BY embedding <=> ai.openai_embed('text-embedding-3-small', %s)
            LIMIT 1;
        """
        cursor.execute(query, (user_query,))
        rows = cursor.fetchall()
        cursor.close()

        # Format results to return only relevant fragments
        fragments = [{"id": row[0], "fragment": row[1]} for row in rows]
        return fragments
    except Exception as e:
        print(f"Error querying database: {e}")
        return []
    finally:
        conn.close()


# Get related chat history fragment
def get_chat_history_fragment(user_query):
    conn = connect_db()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
            SELECT id, ollama_response, embedding
            FROM history_embeddings
            ORDER BY embedding <=> ai.openai_embed('text-embedding-3-small', %s)
            LIMIT 1;
        """
        cursor.execute(query, (user_query,))
        rows = cursor.fetchall()
        cursor.close()

        # Format results to return only relevant fragments
        fragments = [{"id": row[0], "ollama_response": row[1]} for row in rows]
        return fragments
    except Exception as e:
        print(f"Error querying database: {e}")
        return []
    finally:
        conn.close()


# Ollama API call
def get_ollama_response(prompt):
    try:
        response = ollama.chat(
            model="llama3.2", messages=[{"role": "user", "content": prompt}]
        )

        if "message" in response and "content" in response["message"]:
            return response["message"]["content"]
        else:
            return "No response received from Ollama."
    except Exception as e:
        print("Error connecting to Ollama API:", e)
        return "There was an error processing your request."


# Save chat in the db
def save_chat_history(user_query, ollama_response):
    conn = connect_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (user_query, ollama_response) VALUES (%s, %s)",
            (user_query, ollama_response),
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting chat history: {e}")
    finally:
        conn.close()


# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")


# Variable to keep track of the last ollama response
prev_response = None


# Route to handle chatbot queries
@app.route("/chat", methods=["POST"])
def chat():
    global prev_response

    context = ""
    user_query = request.form["query"]

    chat_history_fragment = get_chat_history_fragment(user_query)
    story_fragment = get_story_fragment(user_query)

    if chat_history_fragment and chat_history_fragment != prev_response:
        context += (
            f"Related past story: {chat_history_fragment[0]['ollama_response']}\n"
        )

    if prev_response:
        context += f"Previous story: {prev_response}\n"

    if story_fragment:
        context += f"Current story inspiration: {story_fragment[0]['fragment']}\n"

    context += f"Current query: {user_query}\n"

    context += "Continue the previous story using the current query, the inspiration and the past story."

    ollama_response = get_ollama_response(context)

    save_chat_history(user_query, ollama_response)

    prev_response = ollama_response

    return f"""
    <div class="message user-message">
        <strong>You:</strong> {user_query}
    </div>
    <div class="message bot-message">
        <strong>Bot:</strong> {ollama_response}
    </div>
    """


if __name__ == "__main__":
    app.run(debug=True)
