import os
from dotenv import load_dotenv
from google import genai
from agents.planner import plan
from agents.researcher import research

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
topic = input("Enter your research topic: ")

research_plan = plan(client,topic)
results = []
for question in research_plan.sub_questions:
    result={
        "question" : question,
        "answer" : research(client,question)
    }
    results.append(result)
evidence = {
    "topic": topic,
    "research_results": results
}

print(evidence)
