# Discord RAG Bot

This is a simple Discord bot that uses a **RAG (Retrieval-Augmented Generation)** system to answer questions based on the contents of PDF documents. It combines:

- **Document Chunking**: Splits PDFs into smaller chunks for better semantic search.
- **Embeddings & Vector Store**: Converts chunks into embeddings and stores them in a local FAISS index for fast similarity search.
- **LLM Integration**: Uses an Ollama-hosted LLM (`mistral:7b-instruct`) to generate human-like responses based on the retrieved context.
- **Discord Bot**: Connects to Discord and responds to user commands.

---

## 📂 Project Structure
```plaintext
📂 Project Root
├── bot.py          # Discord bot main entry
├── rag.py          # RAG (retrieval, chunking, embedding) logic
├── requirements.txt
├── .env            # (Not committed) Store your secrets like BOT_TOKEN
├── vectorstores/   # Local FAISS index (created automatically, ignored)
├── pdfs/           # Your source PDF files (ignored)
└── example.txt     # Tracks processed files (ignored)
```
---

## ⚙️ Requirements

- Python 3.9+
- Discord bot token
- Ollama running locally (or your own LLM endpoint)
- PDFs in a `pdfs/` folder

---

## 🛠️ Installation

1. **Clone this repository**

   ```bash
   git clone git@github.com:DurishettyAnirudh/RAG_Bot.git
   cd RAG_Bot


2. **Create and activate a virtual environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows


3. **Install dependencies**

   ```bash
    pip install -r requirements.txt


4. **Create .env**
   ```bash
   BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN

## Running the Bot

1. Make sure your Ollama server is running on http://localhost:11434.
2. Add your PDFs to the pdfs/ folder.
3. Run the bot: python bot.py


## ⚠️ Notes

The vector store and PDF files are ignored from version control (.gitignore).
Keep your .env secret — never commit it!