# AI_AGENT_ENGINE_FROM_SCRATCH
End-To-End robust enterprise-grade GenAI Agent Engine built from scratch [No Langchain or Llamaindex] for Generative AI applications. 
This engine is designed to handle message state, token limits, and AI conversational flow with strict data validation. 

## Tech Stack
* **Language:** Python 3.11+
* **Validation:** Pydantic V2
* **Testing:** Pytest, `pytest-cov`, `pytest-xdist`, `pytest-mock` & Hypothesis

##  Project Structure
```text
AI_AGENT_ENGINE_FROM_SCRATCH/
│
├── src/
│   ├── agent_engine/
│   │   ├── __init__.py
│   │   ├── core/                        # Core components of the engine
│   │   │   ├── __init__.py
│   │   │   ├── message.py               # Message model
│   │   │   ├── conversation.py          # Conversation manager
│   │   │   ├── summarizer.py            # Summarizer component
│   │   │   ├── token_manager.py         # Token manager component
│   │   │   ├── agent.py                 # Agent component
├── test/                                # Unit tests for the engine    
│   ├── __init__.py
│   ├── test_message.py                  # Unit tests for the message model
│   ├── test_conversation.py             # Unit tests for the conversation manager
├── logs/                                # Logs for the engine
├── infrastructure/                      # Infrastructure components (e.g., LLM clients)
├── .env.example                         # Example environment variables
├── .gitignore                           # Git ignore file
├── README.md                            # Project documentation
├── requirments.txt                      # Environmented dependencies
├── Makefile                             # Makefile for common tasks
└── LICENSE                              # License file
```
# Getting started
## clone the repo
```Bash
git clone https://github.com/AhmedSalah309/AI_AGENT_ENGINE_FROM_SCRATCH.git
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

3. **`TokenManager` Model (`src/agent_engine/core/token_manager.py`)**
   - The Token Manager of the engine.
   - Manages the token counting and token management.
   - Handles token estimation and token validation.

4. **`Summarizer` Model (`src/agent_engine/core/summarizer.py`)**
   - The Summarizer of the engine.
   - Manages the summarization and token management.
   - Handles summarization estimation and summarization validation.

5. **`Agent` Model (`src/agent_engine/core/agent.py`)**
   - The Brain of the engine.
   - Manages the conversation flow and interacts with the LLM.
   - Handles streaming responses and token management.
   # Note:
* More components like summarization, tool calling, memory, etc. are under development.

