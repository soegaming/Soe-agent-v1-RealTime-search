import google.generativeai as genai
import os
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
from ddgs import DDGS

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash-lite')
chat = model.start_chat(history=[])
console = Console()

def browsing(query):
    """Fungsi buat cari di DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        if not results:
            return "Ga nemu apa-apa bro di internet."
        
        # Gabungin hasil jadi 1 text
        hasil = ""
        for i, r in enumerate(results, 1):
            hasil += f"{i}. {r['title']}\n{r['body']}\nLink: {r['href']}\n\n"
        return hasil
    except Exception as e:
        return f"Error browsing: {e}"

console.print(Panel.fit(
    "[bold cyan]AI Agent v5.0 - Pake Otak Gemini + Bisa Googling[/]\n"
    "Fitur: ngobrol | ingat | browsing real-time\n"
    "Ketik 'cari xxx' buat browsing, 'exit' buat keluar",
    border_style="green"
))

while True:
    prompt = console.input("[bold yellow]User: [/]")
    
    if prompt.lower() == "exit":
        console.print("[bold red]Dadah bro![/]")
        break
    
    # Cek kalo user mau browsing
    if prompt.lower().startswith("cari "):
        query = prompt[5:]  # Ambil text setelah "cari "
        console.print("[bold blue]Lagi googling...[/]")
        hasil_browsing = browsing(query)
        
        # Kasih hasil browsing ke Gemini buat dirangkum
        prompt_ke_gemini = f"Tolong rangkum hasil pencarian ini dengan bahasa santai buat jawab pertanyaan: {query}\n\nHasil:\n{hasil_browsing}"
        response = chat.send_message(prompt_ke_gemini)
        console.print(f"[bold green]Bot:[/] {response.text}")
    else:
        try:
            response = chat.send_message(prompt)
            console.print(f"[bold green]Bot:[/] {response.text}")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")