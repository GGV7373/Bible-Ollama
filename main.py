import pythonbible as pb
from ollama import chat
from ollama import ChatResponse
import uuid
import os
import requests
import subprocess
import time

# Replace inline book list with a global one so we can validate inputs
BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
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

def books_list():
    # Format books in columns
    columns = 4
    formatted_list = ""
    for i in range(0, len(BOOKS), columns):
        row = BOOKS[i:i + columns]
        formatted_list += "".join(f"{book:<20}" for book in row) + "\n"
    return formatted_list

def start_ollama_if_needed(timeout=60):
    """Try to reach Ollama; if unreachable, start it and poll until available or timeout (seconds)."""
    start_time = time.time()
    server_started = False
    while True:
        try:
            r = requests.get("http://localhost:11434", timeout=1)
            if r.status_code == 200:
                return
        except requests.RequestException:
            if not server_started:
                try:
                    subprocess.Popen(
                        ["ollama", "serve"],
                        start_new_session=True
                    )
                except Exception:
                    # could not start process; continue trying to connect in case it's started externally
                    pass
                server_started = True
        time.sleep(1)
        if time.time() - start_time > timeout:
            print("Warning: Ollama server did not become available within timeout.")
            return

def get_valid_book():
    print("Here are the available books:")
    print(books_list())
    mapping = {b.lower(): b for b in BOOKS}
    while True:
        usr_book = input("Which book do you want? ").strip()
        key = usr_book.lower()
        if key in mapping:
            return mapping[key]
        print("Book not found. Please enter a valid book from the list (try again).")

def get_valid_chapter(book_name):
    """Prompt until a valid chapter number for the given book is provided."""
    book_enum = None
    try:
        book_enum = getattr(pb.Book, book_name.upper())
    except Exception:
        # If conversion fails, keep prompting for book again upstream; but handle gracefully
        raise

    while True:
        usr_chapter = input("Which chapter do you want? ").strip()
        try:
            chap = int(usr_chapter)
        except ValueError:
            print("Please enter a numeric chapter.")
            continue
        try:
            num_verses = pb.get_number_of_verses(book_enum, chap)
            if num_verses and num_verses > 0:
                return chap, num_verses, book_enum
            else:
                print(f"Chapter {chap} not found for {book_name}. Try again.")
        except Exception:
            print(f"Chapter {chap} not found for {book_name}. Try again.")

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
    usr_book = get_valid_book()
else:
    usr_book = get_valid_book()  # still force selection if user says no; keep behavior predictable

search_config = {
    "book": usr_book,
    "chapter": "",
    "verseID": "",
}

usr_chapter, number_of_verses, book_enum = get_valid_chapter(usr_book)
search_config["chapter"] = usr_chapter

book = getattr(pb.Book, search_config["book"].upper())
number_of_verses = pb.get_number_of_verses(book, search_config["chapter"])
reference = pb.NormalizedReference(
    book_enum,
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