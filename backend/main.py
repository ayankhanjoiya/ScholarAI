import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
load_dotenv()

client = genai.Client(
    api_key = os.getenv("GOOGLE_API_KEY")
)

class ResearchPlan(BaseModel):
    topic:str
    sub_questions: list[str]

topic = input("Enter your research topic: ")

response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = f"""create a research plan for the topic : {topic}.
                  Generate 4 important sub-questions that should be investigated.""",
    config = {
        "response_mime_type": "application/json",
        "response_schema": ResearchPlan,    
    }
)

print(response.parsed)