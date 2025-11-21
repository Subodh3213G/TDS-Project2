import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from agent import get_llm_response
import uvicorn
import httpx

app = FastAPI()

# Load secrets directly from Environment Variables (Injected by HF Spaces)
MY_SECRET = os.getenv("MY_SECRET")
MY_EMAIL = os.getenv("MY_EMAIL")

class RequestData(BaseModel):
    email: str
    secret: str
    url: str

@app.get("/")
def read_root():
    return {"status": "API is running. Send POST to /quiz"}

@app.post("/quiz")
async def solve_quiz(data: RequestData):
    # 1. Validate Secret [cite: 87]
    if data.secret != MY_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid Secret")

    # 2. Scrape HTML using Playwright
    # We MUST use --no-sandbox for Docker environments
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page()
        
        try:
            await page.goto(data.url, timeout=60000) # 60s timeout
            await page.wait_for_load_state("networkidle") # Wait for JS [cite: 97]
            
            html_content = await page.content()
            
            # 3. Use LLM Agent to get the answer
            submission_payload = await get_llm_response(html_content, data.url, MY_EMAIL, MY_SECRET)
            
            # 4. Submit the answer
            # Note: In a real test, the submit URL is usually dynamic. 
            # For now, we assume the project demo URL or extracted URL.
            # You can improve this by asking the Agent to extract the submit URL too.
            submit_url = submission_payload.get("submit_url_override") or "https://tds-llm-analysis.s-anand.net/demo/submit"
            
            # Remove the override key before sending if it exists
            if "submit_url_override" in submission_payload:
                del submission_payload["submit_url_override"]

            async with httpx.AsyncClient() as client:
                resp = await client.post(submit_url, json=submission_payload, timeout=30.0)
                result = resp.json()
                
            await browser.close()
            return result

        except Exception as e:
            await browser.close()
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)