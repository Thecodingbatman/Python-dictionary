import os
import requests
from dotenv import load_dotenv, dotenv_values
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

load_dotenv() 
app_id = os.getenv("apiID")
app_key = os.getenv("apikeys")
word = input("Enter a word: ").strip().lower()
language = "en-us"
base_url = "https://od-api-sandbox.oxforddictionaries.com/api/v2"
url = f"{base_url}/entries/{language}/{(word)}"
try:
    response = requests.get(
        url,
        headers={
            "app_id": app_id,
            "app_key":app_key,
            "Accept": "application/json",
        },
        timeout= 30
    )
except requests.RequestException:
    exit("request failed 404")
data = response.json()
found_definition = False

console = Console()
definitions = []

for result in data.get("results", []):
    for lexical_entry in result.get("lexicalEntries", []):
        for entry in lexical_entry.get("entries", []):
            for sense in entry.get("senses", []):
                definitions.extend(sense.get("definitions", []))

if definitions:
    body = Text()
    for i, definition in enumerate(definitions, start=1):
        if i > 1:
            body.append("\n\n")
        body.append(f"{i}. ", style="bold cyan")
        body.append(definition)
    found_definition = True

    console.print(Panel(body, title="Definitions", border_style="blue", padding=(1, 2)))
else:
    console.print("[dim]No definitions found.[/dim]")
    found_definition = False
