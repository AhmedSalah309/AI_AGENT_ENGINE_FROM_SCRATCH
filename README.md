# AI_AGENT_ENGINE_FROM_SCRATCH
End-To-End robust enterprise-grade GenAI Agent Engine built from scratch [No Langchain or Llamaindex] for Generative AI applications. 
This engine is designed to handle message state, token limits, and AI conversational flow with strict data validation. 

## Tech Stack
* **Language:** Python 3.11+
* **Validation:** Pydantic V2

##  Project Structure

AI_AGENT_ENGINE_FROM_SCRATCH/
│
├── src/
│   ├── agent_engine/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── message.py
│   │   │   ├── conversation.py
├── test/
├── infrastructure/
├── .env.example
├── .gitignore
├── README.md
├── requirments.txt
├── Makefile
└── LICENSE

# Getting started
## clone the repo
```Bash
git clone <https://github.com/AhmedSalah309/AI_AGENT_ENGINE_FROM_SCRATCH.git>
cd AI_AGENT_ENGINE_FROM_SCRATCH
```

## Core Components (Current Scope)
1. **`Message` Model (`src/agent_engine/core/message.py`)**
   - The atomic unit of the engine.
   - Strictly validates roles (`system`, `user`, `assistant`, `tool`).
   - Prevents empty payloads and manages token metadata immutably.

2. **`Conversation` Manager (`src/agent_engine/core/conversation.py`)**
   - Acts as the State Manager for the AI Agent.
   - **Sliding Window Algorithm:** Automatically enforces token budgets (`max_tokens`) by evicting the oldest messages when limits are reached.
   - **System Prompt Protection:** Guarantees that `index 0` (if acting as the system prompt) is never evicted during context trimming, preventing "persona loss".
   - **LLM Payload Export:** Cleans and formats internal state into standardized `[{"role": "...", "content": "..."}]` structures ready for OpenAI/Anthropic APIs.

   # Note:
* More components like summarization, tool calling, memory, etc. are under development.