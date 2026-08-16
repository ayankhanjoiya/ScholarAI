from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from tools.basic_tools import get_current_year

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
    contents="What is the capital of France?",
    config=config,
)

if response.function_calls:
    for call in response.function_calls:
        print(f"Gemini requested tool call: {call.name}({call.args})")
        if call.name== "get_current_year":
            result = get_current_year()
            print("Tool Result:",result)
        tool_response = types.Part.from_function_response(
            name="get_current_year",
            response={"result":result},
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents = [
                "What year is it?",
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": result},
                        )
                    ],
                ),
            ],
            config=config
        )
        print("Final answer :" ,response.text)
else:
    print(response.text)

