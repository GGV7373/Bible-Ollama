# Bibel-Ollama

Proverbs-Ollama is a Python project that retrieves any chapter from any book in the Bible, analyzes it using an Ollama language model, and provides an explanation of the chapter's content.

## Features

- Select any book and chapter from the Bible.
- Automatically fetches all verses in the chosen chapter.
- Uses Ollama's Llama3.2 model to generate a summary and explanation of the chapter.
- Saves both the input chapter text and the AI-generated explanation to files for later reference.

## Usage

1. Run `main.py`.
2. Enter the name of the book (e.g., Proverbs, Genesis, John) when prompted.
3. Enter the chapter number when prompted.
4. The program will display the full text of the chapter and an AI-generated explanation.
5. The results are saved in a unique folder under `usr/`.

## Requirements

- `pythonbible` library
- `ollama` Python client
- Ollama server running locally (the script will attempt to start it if needed)

Install dependencies with:
```bash
pip install pythonbible ollama requests
```

## Example

```
Which book do you want? Proverbs
Which chapter do you want? 3
[Chapter text output]
[AI explanation output]
```

## Output Files
- `usr/<unique_id>/input.txt`: Contains the full text of the selected chapter.
- `usr/<unique_id>/output.txt`: Contains the AI-generated explanation.

## Notes
- Make sure you have the Ollama server and the Llama3.2 model available locally.
- The script supports any book and chapter recognized by the `pythonbible` library.
