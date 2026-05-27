import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MEMORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("File memory rusak, bikin baru...") 
            return []
    return []

def save_history(history):
    # Convert object history ke dict biar bisa di-json-in
    history_dict = [msg.to_json_dict() for msg in history]
    with open(MEMORY_FILE, 'w') as f:
        json.dump(history_dict, f, indent=2)

def main():
    chat_history = load_history()
    chat = client.chats.create(model='gemini-2.5-flash', history=chat_history)
    
    print("Soe Agent v2 - Memory Mode 🧠")
    print("Ketik 'reset' buat hapus memori, 'exit' buat keluar")
    print("-" * 40)

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            save_history(chat.get_history())
            print("Memori disimpen. Bye bro!")
            break
            
        if user_input.lower() == 'reset':
            chat = client.chats.create(model='gemini-2.5-flash', history=[])
            if os.path.exists(MEMORY_FILE):
                os.remove(MEMORY_FILE)
            print("Memori direset.")
            continue

        try:
            response = chat.send_message(user_input)
            print(f"Agent: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()