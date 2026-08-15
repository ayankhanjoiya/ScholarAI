import os
from dotenv import load_dotenv
from google import genai
from agents.planner import plan
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
topic = input("Enter your research topic: ")

print(plan(client,topic))
