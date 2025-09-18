# Proverbs-Ollama

Proverbs-Ollama is a Python project that retrieves a chapter from the Book of Proverbs in the Bible, analyzes it using an Ollama language model, and provides an explanation of the chapter's content.

## Features

- Select any chapter (1-31) from Proverbs.
- Automatically fetches all verses in the chosen chapter.
- Uses Ollama's Llama3.2 model to generate a summary and explanation of the chapter.

## Usage

1. Run `main.py`.
2. Enter a chapter number (1-31) when prompted.
3. The program will display the full text of the chapter and an AI-generated explanation.

## Requirements

- `pythonbible` library
- `ollama` Python client

Install dependencies with:
```bash
pip install pythonbible ollama
```

## Example

```
Which book do you want? 1-31: 3
[Chapter text output]
[AI explanation output]
```