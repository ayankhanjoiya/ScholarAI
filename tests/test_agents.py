from dotenv import load_dotenv
load_dotenv()

from google import genai
from agents.researcher import research

client = genai.Client()

with open("tests/agent_questions.text","r",encoding="utf-8") as f:
    questions = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

for i , question in enumerate(questions , 1):
    print("\n" + "=" * 70)
    print(f"TEST {i}")
    print("=" * 70)
    print("Question: " , question)

    answer = research(client , question)

    print("\nFinal Answer: ")
    print(answer)
