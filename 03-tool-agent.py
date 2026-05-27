import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import datetime
import wikipedia

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_current_time():
    """Dapetin waktu sekarang dalam format WIB"""
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    return now.strftime("%H:%M:%S WIB, %d %B %Y")

def search_wikipedia(query: str):
    """Cari info di Wikipedia Indonesia/English untuk data faktual"""
    try:
        wikipedia.set_lang("id")  # Coba Indonesia dulu
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        return summary
    except wikipedia.exceptions.PageError:
        try:
            wikipedia.set_lang("en")  # Kalo ga ada, coba English
            summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
            return summary
        except:
            return f"Ga nemu artikel Wikipedia untuk '{query}'"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Terlalu banyak hasil untuk '{query}'. Coba yg spesifik: {e.options[:3]}"
    except Exception as e:
        return f"Error Wikipedia: {str(e)}"

tools = [get_current_time, search_wikipedia]

chat = client.chats.create(
    model='gemini-2.0-flash',
    config=types.GenerateContentConfig(tools=tools)
)

print("Soe Agent v3 FINAL - Tool Calling Mode 🛠️📚")
print("Agent lu udah bisa baca Wikipedia real-time")
print("Ketik 'exit' buat keluar")
print("-" * 40)

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
        print("Bye bro!")
        break

    try:
        response = chat.send_message(user_input)
        print(f"Agent: {response.text}")
    except Exception as e:
        print(f"Error: {e}")