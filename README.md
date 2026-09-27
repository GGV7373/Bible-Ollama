# Bible-Ollama

Bible-Ollama is a Python command-line app that retrieves any chapter from any book in the Bible, analyzes it using an Ollama language model, and prints an explanation of the chapter's content.

## Features

- Select any book and chapter from the Bible (including books like `1 Samuel` or `Song of Solomon`).
- Automatically fetches all verses in the chosen chapter.
- Uses an Ollama model (default: `llama3.2`) to generate a summary and explanation of the chapter.
- Look up as many chapters as you like in one session.

## Run with Docker (recommended)

You only need [Docker](https://docs.docker.com/get-docker/). Ollama and the model are set up for you.

```bash
docker compose run --rm app
```

The first run downloads the model (~2 GB for `llama3.2`). It is stored in a Docker volume, so later runs start right away.

Use a different model:

```bash
OLLAMA_MODEL=tinyllama docker compose run --rm app
```

Have an NVIDIA GPU? Uncomment the `deploy:` block in `docker-compose.yml` (requires the NVIDIA Container Toolkit).

Stop the Ollama server when you're done:

```bash
docker compose down
```

## Run locally

Requires Python 3 and [Ollama](https://ollama.com) installed.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2
python main.py
```

The script will try to start `ollama serve` itself if it isn't already running.

### Configuration

| Environment variable | Default                  | Description             |
|----------------------|--------------------------|-------------------------|
| `OLLAMA_MODEL`       | `llama3.2`               | Ollama model to use     |
| `OLLAMA_HOST`        | `http://localhost:11434` | Address of the Ollama server |

## Example

```
Welcome to Bible + Ollama!

Do you want to see the list of Bible books? (y/n): n

Which book do you want? Proverbs
Which chapter do you want? 3

Analyzing the chapter with Ollama...

Analysis:
--------------------------------------------------------------------------------
[AI explanation output]
--------------------------------------------------------------------------------
```
