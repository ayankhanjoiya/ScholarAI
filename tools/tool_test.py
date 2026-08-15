from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

client = genai.Client()

get_current_year_tool = types.FunctionDeclaration(
    name="get_current_year",
    description="Returns the current calendar year.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)

tool = types.Tool(
    function_declarations=[get_current_year_tool]
)

config = types.GenerateContentConfig(
    tools=[tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="What year is it?",
    config=config,
)

if response.function_calls:
    for call in response.function_calls:
        print(f"Gemini requested tool call: {call.name}({call.args})")
else:
    print(response.text)

