# 🐞 Debug Assistant (VS Code + RAG Agent)

A **VS Code Extension** that fixes your code by reading your *entire* project context. It uses a **Python Backend** (FastAPI) to search your files and an **AI Agent** (LangChain) to generate fixes.

![Status](https://img.shields.io/badge/Status-Works_on_my_machine-success)

## ⚡️ What it actually does
1.  **Reads your code:** Indexes your local files using AST parsing (smart chunking).
2.  **Thinks:** An AI Agent decides *what* to search for (doesn't just guess).
3.  **Fixes:** Displays the fix directly in VS Code side-by-side.

## 🚀 How to Run (The "TL;DR")

### 1. Start the Brain (Backend)
```bash
cd backend
# Add your OpenAI Key to a .env file first!
python main.py
2. Start the Interface (Frontend)
Bash

cd debug-assistant-client
npm install
npm run compile
# Now press F5 in VS Code to launch the extension.
3. Use It
Highlight broken code.

Cmd+Shift+P -> "Ask AI Debugger".

Type: "Fix this error."

🧪 Testing
Run this to prove it works:

Bash

python backend/simple_evaluate.py
