import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("GENAI_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash")
def generate_twisted_wish(wish:str)->str:
    try:
        prompt = (
            "You are the cursed Monkey's Paw. For each wish, reply with ONLY one darkly witty twist in a single short sentence.\n"
            f"Wish: {wish}\n"
            "Twist:"
        )
        response =model.generate_content(prompt)
        twist=(getattr(response,"text") or "").strip()
        return twist
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the prompt: {e}")
        