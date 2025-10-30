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

def books_list():
    books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
            "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
            "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
            "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
            "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
            "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
            "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
            "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
            "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
            "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
            "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Colossians",
            "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
    
    # Format books in columns
    columns = 4
    formatted_list = ""
    for i in range(0, len(books), columns):
        row = books[i:i + columns]
        formatted_list += "".join(f"{book:<20}" for book in row) + "\n"
    
    return formatted_list

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
print("Welcome to Bible + Ollama!")

anser = input("Do you want to get the boos of the bibele? y/n: ")
if anser.lower() == 'y':
    print("Here are the available books:")
    print(books_list())

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