#!/bin/bash

set -e

echo "🚀 Starting Local PDF Chatbot Setup..."

PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"
REQ_FILE="$PROJECT_DIR/requirements.txt"
DB_DIR="$PROJECT_DIR/vectorstore"

# ---------------------------
# 1️⃣ Python virtualenv
# ---------------------------
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating virtual environment..."
  python3 -m venv venv
else
  echo "✅ Virtual environment already exists"
fi

source venv/bin/activate
echo $VIRTUAL_ENV
# ---------------------------
# 2️⃣ Python dependencies
# ---------------------------
echo "📦 Checking Python dependencies..."
pip install --upgrade pip

if [ -f "$REQ_FILE" ]; then
  venv/bin/python -m pip install langchain
#  pip install -r requirements.txt
  echo "installing dependencies"
else
  echo "❌ requirements.txt not found"
  exit 1
fi

# ---------------------------
# 3️⃣ Ollama check
# ---------------------------
if ! command -v ollama >/dev/null 2>&1; then
  echo "❌ Ollama not installed."
  echo "👉 Install from https://ollama.com"
  exit 1
fi

if ! pgrep -x "ollama" > /dev/null; then
  echo "🧠 Starting Ollama service..."
  ollama serve >/dev/null 2>&1 &
  sleep 3
else
  echo "✅ Ollama already running"
fi

# ---------------------------
# 4️⃣ Ollama models
# ---------------------------
echo "📥 Checking Ollama models..."

if ! ollama list | grep -q mistral; then
  echo "⬇️ Pulling mistral model..."
  ollama pull mistral
else
  echo "✅ mistral model already present"
fi

if ! ollama list | grep -q nomic-embed-text; then
  echo "⬇️ Pulling embedding model..."
  ollama pull nomic-embed-text
else
  echo "✅ embedding model already present"
fi
echo "which python"
which python3
# ---------------------------
# 5️⃣ Vector DB (one-time ingestion)
# ---------------------------
if [ ! -d "$DB_DIR" ]; then
  echo "📄 Vector DB not found. Running ingestion..."
  python ingest.py
else
  echo "✅ Vector DB already exists"
fi

# ---------------------------
# 6️⃣ Run chatbot
# ---------------------------
echo "🤖 Launching chatbot..."
python3.10 chatbot.py