table of contents:
- [AI_AGENT_ENGINE_FROM_SCRATCH](#ai_agent_engine_from_scratch)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [Ports & Networking Stack](#ports--networking-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting started](#getting-started)
- [Core Components (Current Scope)](#core-components-current-scope)
- [Troubleshooting](#troubleshooting)

# AI_AGENT_ENGINE_FROM_SCRATCH
End-To-End robust enterprise-grade GenAI Agent Engine built from scratch [No Langchain or Llamaindex] for Generative AI applications. 
This engine is designed to handle message state, token limits, and AI conversational flow with strict data validation. 

## Tech Stack
* **Environment:** WSL (Ubuntu)
* **Language:** Python 3.11+
* **Validation:** Pydantic V2
* **Testing:** Pytest, `pytest-cov`, `pytest-xdist`, `pytest-mock` & Hypothesis
* **Code Quality:** Black (Formatting), Ruff (Linting), MyPy (Static Type Checking)
* **AI Model:** Google Gemma:2b (via Ollama)
* **Communication:** RESTful API (JSON)
* **WebFramework:** Flask 3.0.2
* **WSGI Server:** Gunicorn
* **Monitoring:** Prometheus, Grafana
* **Reverse Proxy:** Nginx
* **Database:** SQLite (Local) via SQLAlchemy ORM
* **Migrations:** Alembic
* **Task/Message Queue:** Redis, Celery
* **Containerization:** Docker & Docker Compose

### API Endpoints

To reach the API, prefix the endpoint with your active base URL (e.g., `http://localhost:8002`).

| Method | Endpoint Blueprint | Description |
|--------|--------------------|-------------|
| `GET`  | `/health` | Application health status and current configuration version. |
| `GET`  | `/api/v1/chat/<session_id>` | HTML Frontend Chat UI. |
| `POST` | `/api/v1/chat/<session_id>` | Core conversational Agent engine (Streams SSE responses). |
| `GET`  | `/metrics` | Exposed Prometheus metrics for the Grafana dashboard. |
| `GET`  | `/apidocs` | Swagger UI Documentation *(Coming Soon)* |

## Ports & Networking Stack

| Service | Local Dev Mode (`make run-dev`) | Docker Mode (`make docker-up`) |
|---------|---------------------------------|--------------------------------|
| **Core Web App** | `http://localhost:8002` | `http://localhost:8001` (via Nginx Gateway) |
| **Prometheus** | Not Available | `http://localhost:9091` |
| **Grafana** | Not Available | `http://localhost:3001` (Login: admin/admin) |
| **Redis** | Not Available | `localhost:6380` |
| **Celery** | Not Available | `localhost:5555` |

##  Project Structure
```text
AI_AGENT_ENGINE_FROM_SCRATCH/
│
├── src/
│   ├── agent_engine/
│   │   ├── __init__.py
│   │   ├── api/                         # API components
│   │   │   ├── __init__.py
│   │   │   ├── templates/               # API templates
│   │   │   │   ├── __init__.py
│   │   │   │   └── index.html           # API index template
│   │   │   │
│   │   │   ├── main.py                  # Main API file
│   │   │   ├── routes.py                # API routes
│   │   │   └── schemas.py               # API schemas
│   │   │
│   │   ├── core/                        # Core components of the engine
│   │   │   ├── __init__.py
│   │   │   ├── message.py               # Message model
│   │   │   ├── conversation.py          # Conversation manager
│   │   │   ├── summarizer.py            # Summarizer component
│   │   │   ├── token_manager.py         # Token manager component
│   │   │   ├── agent.py                 # Agent component
│   │   │   ├── celery_app.py            # Celery Application
│   │   │   └── tasks.py                 # Celery Tasks
│   │   │   
│   │   ├── database/                    # Database Layer 
│   │   │   ├── __init__.py
│   │   │   ├── models.py                # Database Models (Tables)
│   │   │   ├── session.py               # Database connection
│   │   │   └── sql_repository.py        # SQL Repository (file storage)
│   │   │
│   │   ├── config/                      # Configuration Layer
│   │   │   ├── __init__.py
│   │   │   ├── settings.py              # Settings Configuration
│   │   │   └── logger.py                # Logger Configuration
│
├── test/                                # Unit tests for the engine    
│   ├── __init__.py
│   ├── test_message.py                  # Unit tests for the message model
│   ├── test_conversation.py             # Unit tests for the conversation manager
│   ├── test_token_manager.py            # Unit tests for the token manager
│   ├── test_summarizer.py               # Unit tests for the summarizer
│   └── test_agent.py                    # Unit tests for the agent
│   
├── logs/                                # Logs for the engine
│   ├── pytest_run.log                   # This file will be created automaticlly when the tests are run
│   └── test_report.txt                  # covrage report 
│
├── infrastructure/                      # Infrastructure components 
│   ├── grafana/                         # Grafana 
│   │   └── grafana.ini                  # Grafana configuration
│   ├── nginx/                           # Nginx 
│   │   └── nginx.conf                   # Nginx configuration
│   └── prometheus/                      # Prometheus 
│       └── prometheus.yml               # Prometheus configuration
│
├── Dockerfile                           # Dockerfile for the application
├── docker-compose.yml                   # Docker Compose for the application
├── .env.example                         # Example environment variables
├── .gitignore                           # Git ignore file
├── README.md                            # Project documentation
├── requirments.txt                      # Environmented dependencies
├── Makefile                             # Makefile for common tasks
├── pyproject.toml                       # Project configuration (Tools settings (Black, Ruff, MyPy))
├── alembic.ini                          # Alembic configuration (This file will be created automaticlly when the make alembic-init are run)
└── LICENSE                              # License file
```
# Prerequisites
## 1- WSL (Windows Subsystem for Linux)
#### 1.1 You need to download WSL by running this command in powershell : `wsl --install`
#### 1.2 Set it to wsl2 by running this command in powershell : `wsl --set-default-version 2`
#### 1.3 Make sure it is wsl2 by running this command in powershell : `wsl --version`
#### 1.4 Install a specific distribution of linux (ubuntu) by running this command in powershell : `wsl --install -d ubuntu`
#### 1.5 Open start menu and search for ubuntu and open it
* **Note : At the first time it will ask you to create a username and password. and this password will be used to run any command with sudo (administrator) privileges.**
If you forgot linux password please click : [Troubleshooting](#Troubleshooting--forgot-linux-password)
#### 1.6 Update and upgrade the linux system by running the following command in ubuntu terminal:
```bash
sudo apt update && sudo apt upgrade -y
```
#### 1.7 to open your project folder in wsl you can use the following command:
```bash
cd /Your project folder path
```
#### 1.8 to open vscode or antigravity or cursor in wsl you can use the following command:
```bash
code .
```
```bash
antigravity .
```
```bash
cursor .
```
#### 1.9 finally to make sure that you have installed wsl2 correctly you can run the following command:
```bash
uname -a
```
**Output should be like this (the name of the computer and the version of the kernel may be different):**
```
Linux DESKTOP-Q79ANCI 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```
* finally you have alot of terminals to use and we are going to use ubuntu terminal for the rest of the project.
![alt text](<Screenshot (273).png>)

## 2- Docker setup 
#### 2.1- **You need to download Docker desktop via this link** : https://www.docker.com/products/docker-desktop/
* Then sign in with your docker account
#### 2.2- Access WSL integration in docker desktop (for windows 11) : 
go to settings -> resources -> WSL integration -> enable WSL integration
![alt text](<Screenshot (272).png>)
#### 2.3- Apply and restart docker desktop
#### 2.4- Now open wsl and you can check for docker version by running `docker compose version`

## 3- make setup
* The most efficient way to install make on a WSL (Ubuntu) system is by installing the build-essential package, which includes make, gcc, and other necessary compilation tools:
```bash
sudo apt install build-essential
```
* Alternatively, if you only want make, you can run:
```bash
sudo apt install make
```
* Verify the Installation
Check that make is installed correctly by running:
```bash
make --version
```

# 4- ollama setup
* **Since this project uses a local LLM (Google Gemma:2b)** : you need to set up the ollama environment first inside your WSL environment.
* **4.1 Install Ollama in WSL**
Run the following command in your WSL terminal:
```Bash
curl -fsSL https://ollama.com/install.sh | sh
```
- **Note on permission:** when prompted for `[sudo] password`, enter your Linux user password.
* **4.2 Download & Run Gemma 2B Model**
```bash
ollama run gemma:2b # I used this model, you can use any other model like (llama3,mistral,phi3,etc)
```
* **Note :** The first time you run this command, it will take some time to download the model it depends on your internet speed and the model size.
* **To exit the model interface** : Type `/bye` and press `Enter`.
* **To stop the ollama service** : it will run in the background.if you need to stop it,but you can still use it in the background, run the following command:
```bash
ollama stop
```
* **To run the ollama service again**, run the following command:
```bash
ollama run gemma:2b # or any other model name you downloaded
```
* **but if you want to end the ollama service completely**, run the following command:
```bash
sudo systemctl stop ollama
```
* **To start the ollama service again**, run the following command:
```bash
sudo systemctl start ollama
```

# Getting started

## 1- clone the repo
```Bash
git clone https://github.com/AhmedSalah309/AI_AGENT_ENGINE_FROM_SCRATCH.git
```
Then :
```Bash
cd AI_AGENT_ENGINE_FROM_SCRATCH
```
## 2- setup the environment
* I use standard python virtual environment (`.venv`) and a `Makefile` to manage the development workflow.
```Bash
make setup
```
## 3- Running the Server
* Start the Flask development server with auto reload
```Bash
make run-dev
```
* The server will be live at `http://localhost:8002`
* Health check endpoint: `http://localhost:8002/health`
* Chat endpoint: `http://localhost:8002/api/v1/chat/test_session`
* Swagger UI: `http://localhost:8002/apidocs`

## 4- Build the Docker image
```Bash
make docker-build
```
## 5- Run the Docker container
```Bash
make docker-up
```

## Troubleshooting : Forgot Linux password?
if you don't know your linux password, follow these steps in **Windows PowerShell** (not WSL):
* **close all WSL terminals**
* **open PowerShell as administrator and set the default user to root:**
```powershell
wsl -u root
```
* **Inside the root terminal, run the following command to reset the password:**
```bash
passwd <your-wsl-username>
```
* **Exit and set the default user back(optional):**
```bash
wsl --set-default-user <your-username>
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
* tool registry,Prompt builder, RAG, Vector DB and docker(test) are under development.



