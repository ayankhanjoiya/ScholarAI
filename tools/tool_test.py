import os
from google import genai
from dotenv import load_dotenv
from tools.basic_tools import get_current_year

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = "what is the current year?",
        config = {
            "tools" : [get_current_year]
        }
)
print(response.text)