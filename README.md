# File_Finder_AI_Agent

Search your PDFs by content, not just filenames — using LLaMA, LangChain, and FAISS.
Runs entirely locally, respects your privacy, and gives answers in under 10 seconds.


## Features
🔍 Ask: “Find the PDF that talks about flight bookings”

🧠 LLaMA reasons through PDF content

⚡ FAISS filters top results before invoking the LLM

🔒 Runs 100% locally via Ollama


## Performance
Method	Time (20 PDFs)
Brute Force	~25s
Hybrid (FAISS + LLM)	~9s ✅

## How It Works
PDFs are indexed with FAISS

At query time, FAISS finds top matches

LLaMA agent confirms content relevance

You get accurate results — fast


## All Local. All Private.
No cloud. No leaks. Just fast, private AI magic.
