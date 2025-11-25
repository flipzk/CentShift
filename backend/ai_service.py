import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Configure Google Gemini
if not API_KEY:
    print("Warning: GOOGLE_API_KEY not found in .env file")
else:
    genai.configure(api_key=API_KEY)

def analyze_receipt(image_bytes):
    """
    Sends the image to Google Gemini and expects a JSON response
    with transaction details.
    """
    if not API_KEY:
        return {"error": "API Key missing"}

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')        
        image = Image.open(io.BytesIO(image_bytes))

        # The Prompt: Strict instructions for the AI
        prompt = """
        Analyze this receipt image and extract the following data in strict JSON format:
        
        1. "total": The total amount paid (float).
        2. "date": Date in YYYY-MM-DD format (use today's date if not visible).
        3. "description": Merchant name or brief summary.
        4. "category": Choose exactly ONE from this list: 
           ["Expenses (Necessities)", "Personal (Wants)", "Investments", "Savings (Emergency Fund)", "Income", "Other"]
        
        Return ONLY the raw JSON. No markdown formatting (like ```json), just the object.
        """

        response = model.generate_content([prompt, image])
        
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_text)

    except Exception as e:
        print(f"AI Error: {e}")
        return {"error": str(e)}