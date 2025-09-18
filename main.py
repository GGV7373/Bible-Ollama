import pythonbible as pb
from ollama import chat
from ollama import ChatResponse
import uuid
import os
import requests
import subprocess
import time

def start_ollama_if_needed():
    try:
        requests.get("http://localhost:11434")
    except:
        subprocess.Popen(
            ["ollama", "serve"],
            start_new_session=True
        )
        time.sleep(5)

search_config = {
    "book": "",
    "chapter": "",
    "verseID": "",
}

search_results = {
    "verses_param": 0,
    "verses": [],
    "context": "",
}


# QUESTIONS ----------------------------------------
usr_book = input("Which book do you want? ") 
search_config["book"] = usr_book

usr_chapter = int(input("Which chapter do you want? "))
search_config["chapter"] = usr_chapter

book = getattr(pb.Book, search_config["book"].upper())
number_of_verses = pb.get_number_of_verses(book, search_config["chapter"])
reference = pb.NormalizedReference(
    book,
    search_config["chapter"],
    1,
    search_config["chapter"],
    number_of_verses
)
verse_ids = pb.convert_reference_to_verse_ids(reference)
search_config["verseID"] = verse_ids

search_results = {"verses_param": len(verse_ids), "verses": [], "context": ""}

# RETREIVE ALL VERSES ------------------------------
for vid in verse_ids:
    txt = pb.get_verse_text(vid)
    search_results["verses"].append(txt)
    search_results["context"] += txt + "\n"

# ANALYZE CONTEXT ------------------------------
start_ollama_if_needed()
response: ChatResponse = chat(
    model='llama3.2',
    messages=[
        {
            'role': 'user',
            'content': f"{search_results['context']}\n\nExplain this chapter of {search_config['book']}. Give me the text and explanation."
        },
    ],
)

# PRINT ANALYSIS ---------------------------------

base_path = f"usr/{uuid.uuid4()}"
os.makedirs(base_path, exist_ok=True)

print(response['message']['content'])
with open(f"{base_path}/output.txt", "w") as f:
    f.write(response['message']['content'])

with open(f"{base_path}/input.txt", "w") as f:
    f.write(search_results['context'])