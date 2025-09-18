import pythonbible as bible
from ollama import chat
from ollama import ChatResponse

# Returns the starting verse number for a given chapter in Proverbs
def book_bible(bible_book): 
    if bible_book == 1:
        return 20001001
    elif bible_book == 2:
        return 20002001
    elif bible_book == 3:
        return 20003001
    elif bible_book == 4:
        return 20004001
    elif bible_book == 5:
        return 20005001
    elif bible_book == 6:
        return 20006001
    elif bible_book == 7:
        return 20007001
    elif bible_book == 8:
        return 20008001
    elif bible_book == 9:
        return 20009001
    elif bible_book == 10:
        return 20010001
    elif bible_book == 11:
        return 20011001
    elif bible_book == 12:
        return 20012001
    elif bible_book == 13:
        return 20013001
    elif bible_book == 14:
        return 20014001
    elif bible_book == 15:
        return 20015001
    elif bible_book == 16:
        return 20016001
    elif bible_book == 17:
        return 20017001
    elif bible_book == 18:
        return 20018001
    elif bible_book == 19:
        return 20019001
    elif bible_book == 20:
        return 20020001
    elif bible_book == 21:
        return 20021001
    elif bible_book == 22:
        return 20022001
    elif bible_book == 23:
        return 20023001
    elif bible_book == 24:
        return 20024001
    elif bible_book == 25:
        return 20025001
    elif bible_book == 26:
        return 20026001
    elif bible_book == 27:
        return 20027001
    elif bible_book == 28:
        return 20028001
    elif bible_book == 29:
        return 20029001
    elif bible_book == 30:
        return 20030001
    elif bible_book == 31:
        return 20031001
    return None

# Variable to store the complete chapter text
book_complite = ""

# Prompt user for the chapter number in Proverbs
bible_book = int(input("Which book do you want? 1-31: ")) 

# Get the starting verse number for the selected chapter
bible_verse = book_bible(bible_book)

if bible_verse is None:
    print("Invalid book number.")
    exit()

# Count the number of verses in the selected chapter
count = bible.get_number_of_verses(bible.Book.PROVERBS, chapter=bible_book) # count the number of verses

# Retrieve all verses in the selected chapter and concatenate them
for i in range(count):
    vers_get =  bible.get_verse_text(bible_verse)
    book_complite += vers_get
    bible_verse += 1  # Move to the next verse

# Print the complete chapter text
print(book_complite)

# Use the Ollama model to analyze the Proverbs chapter
response: ChatResponse = chat(
    model='llama3.2',
    messages=[
        {
            'role': 'user',
            'content': f"{book_complite}\n\nExplain this chapter of Proverbs. Give me the text and explanation."
        },
    ],
)

print(response['message']['content'])