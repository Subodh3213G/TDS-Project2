import httpx
import pandas as pd
import PyPDF2
import io

async def process_file_from_url(file_url: str):
    """Downloads and extracts text/data from PDF or CSV URLs."""
    try:
        # Follow redirects is important for some download links
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(file_url)
            
        # Basic extension check
        if file_url.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
            text = ""
            # Extract text from first 5 pages max to save time/tokens
            for i, page in enumerate(pdf_reader.pages):
                if i > 5: break 
                text += page.extract_text()
            return f"PDF Content: {text[:4000]}" 
            
        elif file_url.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(response.content))
            # Return markdown table (more token efficient than raw CSV sometimes)
            return f"CSV Data Head:\n{df.head(20).to_markdown()}"
            
        else:
            return "Error: Unsupported file format. Only PDF/CSV supported."
    except Exception as e:
        return f"Error downloading/processing file: {str(e)}"