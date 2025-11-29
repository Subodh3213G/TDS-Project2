metadata
title: TDS2
emoji: 🏃
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
LLM Analysis - Autonomous Quiz Solver Agent
License: MIT Python 3.12+ FastAPI

An intelligent, autonomous agent built with LangGraph and LangChain that solves data-related quizzes involving web scraping, data processing, analysis, and visualization tasks. The system uses Google's Gemini 2.5 Flash model to orchestrate tool usage and make decisions.

📋 Table of Contents
Overview
Architecture
Features
Project Structure
Installation
Configuration
Usage
API Endpoints
Tools & Capabilities
Docker Deployment
How It Works
License
🔍 Overview
This project was developed for the TDS (Tools in Data Science) course project, where the objective is to build an application that can autonomously solve multi-step quiz tasks involving:

Data sourcing: Scraping websites, calling APIs, downloading files
Data preparation: Cleaning text, PDFs, and various data formats
Data analysis: Filtering, aggregating, statistical analysis, ML models
Data visualization: Generating charts, narratives, and presentations
The system receives quiz URLs via a REST API, navigates through multiple quiz pages, solves each task using LLM-powered reasoning and specialized tools, and submits answers back to the evaluation server.

🏗️ Architecture
The project uses a LangGraph state machine architecture with the following components:

┌─────────────┐
│   FastAPI   │  ← Receives POST requests with quiz URLs
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Agent     │  ← LangGraph orchestrator with Gemini 2.5 Flash
│   (LLM)     │
└──────┬──────┘
       │
       ├────────────┬────────────┬─────────────┬──────────────┐
       ▼            ▼            ▼             ▼              ▼
   [Scraper]   [Downloader]  [Code Exec]  [POST Req]  [Add Deps]
Key Components:
FastAPI Server (main.py): Handles incoming POST requests, validates secrets, and triggers the agent
LangGraph Agent (agent.py): State machine that coordinates tool usage and decision-making
Tools Package (tools/): Modular tools for different capabilities
LLM: Google Gemini 2.5 Flash with rate limiting (9 requests per minute)
✨ Features
✅ Autonomous multi-step problem solving: Chains together multiple quiz pages
✅ Dynamic JavaScript rendering: Uses Playwright for client-side rendered pages
✅ Code generation & execution: Writes and runs Python code for data tasks
✅ Flexible data handling: Downloads files, processes PDFs, CSVs, images, etc.
✅ Self-installing dependencies: Automatically adds required Python packages
✅ Robust error handling: Retries failed attempts within time limits
✅ Docker containerization: Ready for deployment on HuggingFace Spaces or cloud platforms
✅ Rate limiting: Respects API quotas with exponential backoff
📁 Project Structure
LLM-Analysis-TDS-Project-2/
├── agent.py                    # LangGraph state machine & orchestration
├── main.py                     # FastAPI server with /solve endpoint
├── pyproject.toml              # Project dependencies & configuration
├── Dockerfile                  # Container image with Playwright
├── .env                        # Environment variables (not in repo)
├── tools/
│   ├── __init__.py
│   ├── web_scraper.py          # Playwright-based HTML renderer
│   ├── code_generate_and_run.py # Python code executor
│   ├── download_file.py        # File downloader
│   ├── send_request.py         # HTTP POST tool
│   └── add_dependencies.py     # Package installer
└── README.md
📦 Installation
Prerequisites
Python 3.12 or higher
uv package manager (recommended) or pip
Git
Step 1: Clone the Repository
git clone https://github.com/saivijayragav/LLM-Analysis-TDS-Project-2.git
cd LLM-Analysis-TDS-Project-2
Step 2: Install Dependencies
Option A: Using uv (Recommended)
Ensure you have uv installed, then sync the project:

# Install uv if you haven't already  
pip install uv

# Sync dependencies  
uv sync
uv run playwright install chromium
Start the FastAPI server:

uv run main.py
The server will start at http://0.0.0.0:7860.

Option B: Using pip
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install chromium
⚙️ Configuration
Environment Variables
Create a .env file in the project root:

# Your credentials from the Google Form submission
EMAIL=your.email@example.com
SECRET=your_secret_string

# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here
Getting a Gemini API Key
Visit Google AI Studio
Create a new API key
Copy it to your .env file
🚀 Usage
Local Development
Start the FastAPI server:

# If using uv
uv run main.py

# If using standard Python
python main.py
The server will start on http://0.0.0.0:7860

Testing the Endpoint
Send a POST request to test your setup:

curl -X POST http://localhost:7860/solve \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "your_secret_string",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
Expected response:

{
  "status": "ok"
}
The agent will run in the background and solve the quiz chain autonomously.

🌐 API Endpoints
POST /solve
Receives quiz tasks and triggers the autonomous agent.

Request Body:

{
  "email": "your.email@example.com",
  "secret": "your_secret_string",
  "url": "https://example.com/quiz-123"
}
Responses:

Status Code	Description
200	Secret verified, agent started
400	Invalid JSON payload
403	Invalid secret
GET /healthz
Health check endpoint for monitoring.

Response:

{
  "status": "ok",
  "uptime_seconds": 3600
}
🛠️ Tools & Capabilities
The agent has access to the following tools:

1. Web Scraper (get_rendered_html)
Uses Playwright to render JavaScript-heavy pages
Waits for network idle before extracting content
Returns fully rendered HTML for parsing
2. File Downloader (download_file)
Downloads files (PDFs, CSVs, images, etc.) from direct URLs
Saves files to LLMFiles/ directory
Returns the saved filename
3. Code Executor (run_code)
Executes arbitrary Python code in an isolated subprocess
Returns stdout, stderr, and exit code
Useful for data processing, analysis, and visualization
4. POST Request (post_request)
Sends JSON payloads to submission endpoints
Includes automatic error handling and response parsing
Prevents resubmission if answer is incorrect and time limit exceeded
5. Dependency Installer (add_dependencies)
Dynamically installs Python packages as needed
Uses uv add for fast package resolution
Enables the agent to adapt to different task requirements
🐳 Docker Deployment
Build the Image
docker build -t llm-analysis-agent .
Run the Container
docker run -p 7860:7860 \
  -e EMAIL="your.email@example.com" \
  -e SECRET="your_secret_string" \
  -e GOOGLE_API_KEY="your_api_key" \
  llm-analysis-agent
Deploy to HuggingFace Spaces
Create a new Space with Docker SDK
Push this repository to your Space
Add secrets in Space settings:
EMAIL
SECRET
GOOGLE_API_KEY
The Space will automatically build and deploy
🧠 How It Works
1. Request Reception
FastAPI receives a POST request with quiz URL
Validates the secret against environment variables
Returns 200 OK and starts the agent in the background
2. Agent Initialization
LangGraph creates a state machine with two nodes: agent and tools
The initial state contains the quiz URL as a user message
3. Task Loop
The agent follows this loop:

┌─────────────────────────────────────────┐
│ 1. LLM analyzes current state           │
│    - Reads quiz page instructions       │
│    - Plans tool usage                   │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ 2. Tool execution                       │
│    - Scrapes page / downloads files     │
│    - Runs analysis code                 │
│    - Submits answer                     │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ 3. Response evaluation                  │
│    - Checks if answer is correct        │
│    - Extracts next quiz URL (if exists) │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ 4. Decision                             │
│    - If new URL exists: Loop to step 1  │
│    - If no URL: Return "END"            │
└─────────────────────────────────────────┘
4. State Management
All messages (user, assistant, tool) are stored in state
The LLM uses full history to make informed decisions
Recursion limit set to 200 to handle long quiz chains
5. Completion
Agent returns "END" when no new URL is provided
Background task completes
Logs indicate success or failure
📝 Key Design Decisions
LangGraph over Sequential Execution: Allows flexible routing and complex decision-making
Background Processing: Prevents HTTP timeouts for long-running quiz chains
Tool Modularity: Each tool is independent and can be tested/debugged separately
Rate Limiting: Prevents API quota exhaustion (9 req/min for Gemini)
Code Execution: Dynamically generates and runs Python for complex data tasks
Playwright for Scraping: Handles JavaScript-rendered pages that requests cannot
uv for Dependencies: Fast package resolution and installation
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

Author: Sai Vijay Ragav Course: Tools in Data Science (TDS) Institution: IIT Madras

For questions or issues, please open an issue on the GitHub repository.
