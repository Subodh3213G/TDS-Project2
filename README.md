# TDS Automated Quiz Solver  
**FastAPI + Playwright + OpenAI LLM Agent**

 **Live Demo:** https://subodh0912-tds2.hf.space/  
This repository contains an automated quiz-solving backend that renders dynamic quiz pages, extracts data, solves questions using an LLM agent, processes files (PDF/CSV), and finally submits the answer automatically.

---

## Features

### 1. Full Website Rendering (JS Enabled)
Uses **Playwright Chromium** to load JavaScript-heavy quiz pages and extract full HTML.

### 2. LLM-Powered Multi-Step Agent  
The agent:
1. Reads HTML  
2. Decides:  
   - *Solve directly*, or  
   - *Download attached file*  
3. Processes PDFs/CSVs  
4. Produces final answer  
5. Submits result to quiz endpoint  

### 3. File Processing
- PDF → Extracted text (first 5 pages)  
- CSV → DataFrame preview  

### 4. FastAPI Backend
Exposes one main endpoint:

```
POST /quiz
```

Which accepts:

```json
{
  "email": "...",
  "secret": "...",
  "url": "https://..."
}
```

---

## Project Structure

```
.
├── agent.py           # Main LLM reasoning engine
├── main.py            # FastAPI server + Playwright renderer + submission
├── tools.py           # PDF/CSV processing utilities
├── requirements.txt   # Python dependencies
├── Dockerfile         # For containerized deployment
├── .gitattributes     # Git LFS patterns
└── ci.yml             # CI config
```

---

## Environment Variables (Required)

Set these before running the server:

| Variable        | Purpose |
|----------------|---------|
| `OPENAI_API_KEY` | LLM access |
| `MY_SECRET`      | Auth for `/quiz` endpoint |
| `MY_EMAIL`       | Email included in submissions |

Example:
```bash
export OPENAI_API_KEY="sk-xxxx"
export MY_SECRET="your-secret"
export MY_EMAIL="you@example.com"
```

---

## Running Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Playwright browsers
```bash
python -m playwright install
```

### 3. Start server
```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

---

## Example API Request

```bash
curl -X POST http://localhost:7860/quiz   -H "Content-Type: application/json"   -d '{
    "email": "you@example.com",
    "secret": "your-secret",
    "url": "https://example.com/quiz"
  }'
```

---

## Docker Usage

Build:
```bash
docker build -t tds-agent .
```

Run:
```bash
docker run -p 7860:7860   -e OPENAI_API_KEY=your_api_key   -e MY_SECRET=your_secret   -e MY_EMAIL=you@example.com   tds-agent
```

---

## Deployment (HuggingFace Space)

This project is deployed at:

👉 **https://subodh0912-tds2.hf.space/**  

Make sure you configure your **Environment Variables** inside the HF Space settings.

---

## Notes / Limitations

- The LLM agent returns an error if `OPENAI_API_KEY` is missing (intentional safety).  
- Only **PDF** and **CSV** files are processed.  
- Playwright requires system dependencies (already handled in Dockerfile).  
- The agent falls back to a demo submit URL if none is found.

---

## License
You may add MIT or Apache-2.0 as per your preference.

---

## Contributing
Pull requests are welcome — feel free to improve extraction quality, add file support, or optimize agent logic.

---

## If you like the project
Don’t forget to **star** ⭐ the repository on GitHub after uploading!
