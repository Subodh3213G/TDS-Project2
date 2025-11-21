import os
import json
from openai import OpenAI
from tools import process_file_from_url

# --- SAFELY INITIALIZE CLIENT ---
# Instead of crashing immediately, we check if the key exists.
api_key = os.getenv("OPENAI_API_KEY")
client = None

if api_key:
    client = OpenAI(api_key=api_key)
else:
    print("WARNING: OPENAI_API_KEY not found. Agent will fail if called.")
# --------------------------------

async def get_llm_response(html_content: str, current_url: str, email: str, secret: str):
    
    # 1. Fail Gracefully if key is missing
    if not client:
        print("Error: Attempted to use LLM without API Key.")
        return {
            "email": email,
            "secret": secret,
            "url": current_url,
            "answer": "Server Error: OPENAI_API_KEY is missing in server configuration."
        }

    # --- STEP 1: PLAN ---
    system_prompt_1 = """
    You are an automated data extraction agent. 
    Analyze the provided HTML content.
    1. Identify the core question.
    2. Identify if a file download (PDF/CSV) is REQUIRED.
    3. Identify the submission URL.

    Output JSON ONLY:
    {
        "action": "download" OR "answer",
        "file_url": "https://..." (if action is download),
        "submit_url": "https://..." (if found),
        "reasoning_answer": "Answer string" (if action is answer)
    }
    """
    
    # Truncate HTML to avoid token limits
    truncated_html = html_content[:15000] 
    
    try:
        response_1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt_1},
                {"role": "user", "content": f"HTML content: {truncated_html}"}
            ],
            response_format={"type": "json_object"}
        )
        
        plan = json.loads(response_1.choices[0].message.content)
        final_answer = None
        
        # --- STEP 2: EXECUTE ---
        if plan.get("action") == "download" and plan.get("file_url"):
            print(f"Agent downloading: {plan['file_url']}")
            file_summary = await process_file_from_url(plan['file_url'])
            
            system_prompt_2 = "Use the file data to answer the question. Return JSON: {'answer': 'result'}"
            user_prompt_2 = f"Question Context: {current_url}\n\nFile Data:\n{file_summary}"
            
            response_2 = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt_2},
                    {"role": "user", "content": user_prompt_2}
                ],
                response_format={"type": "json_object"}
            )
            final_answer = json.loads(response_2.choices[0].message.content).get("answer")
        else:
            final_answer = plan.get("reasoning_answer")

        # --- STEP 3: FORMAT ---
        return {
            "email": email,
            "secret": secret,
            "url": current_url,
            "answer": final_answer,
            "submit_url_override": plan.get("submit_url") 
        }

    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "email": email,
            "secret": secret,
            "url": current_url,
            "answer": f"Error generating response: {str(e)}"
        }