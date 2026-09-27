import pythonbible as pb
from ollama import chat
from ollama import ChatResponse
import os
import requests
import subprocess
import time
from urllib.parse import urlparse

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

def ollama_is_up():
    try:
        requests.get(OLLAMA_HOST, timeout=2)
        return True
    except requests.RequestException:
        return False

def start_ollama_if_needed():
    if ollama_is_up():
        return
    # Only try to start a server ourselves if it's supposed to be local
    if urlparse(OLLAMA_HOST).hostname not in ("localhost", "127.0.0.1"):
        return
    subprocess.Popen(
        ["ollama", "serve"],
        start_new_session=True
    )
    for _ in range(30):
        if ollama_is_up():
            return
        time.sleep(0.5)

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
            "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
            "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
    
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

def process_chapter_lookup():
    try:
        anser = input("\nDo you want to see the list of Bible books? (y/n): ")
        if anser.lower() == 'y':
            print("\nHere are the available books:")
            print(books_list())

        usr_book = input("\nWhich book do you want? ").strip()
        search_config["book"] = usr_book

        usr_chapter = int(input("Which chapter do you want? "))
        search_config["chapter"] = usr_chapter

        references = pb.get_references(f"{usr_book} {usr_chapter}")
        if not references:
            raise ValueError("Unknown book")
        book = references[0].book
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

        for vid in verse_ids:
            txt = pb.get_verse_text(vid)
            search_results["verses"].append(txt)
            search_results["context"] += txt + "\n"

        print("\nAnalyzing the chapter with Ollama...")
        start_ollama_if_needed()
        response: ChatResponse = chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    'role': 'user',
                    'content': f"{search_results['context']}\n\nExplain this chapter of {search_config['book']}. Give me the text and explanation."
                },
            ],
        )

        # Print analysis instead of saving to files
        print("\nAnalysis:")
        print("-" * 80)
        print(response['message']['content'])
        print("-" * 80)

        return True  # Continue the loop

    except (AttributeError, ValueError):
        print("\nError: Invalid book or chapter. Please try again.")
        return True
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return True


def main():
    print("Welcome to Bible + Ollama!")
    
    while True:
        if not process_chapter_lookup():
            break
            
        again = input("\nWould you like to look up another chapter? (y/n): ")
        if again.lower() != 'y':
            print("\nThank you for using Bible + Ollama. Goodbye!")
            break

if __name__ == "__main__":
    main()
