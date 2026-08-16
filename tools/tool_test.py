from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from tools.basic_tools import get_current_year,get_current_month

client = genai.Client()

get_current_year_tool = types.FunctionDeclaration(
    name="get_current_year",
    description="Returns the current calendar year.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)

get_current_month_tool = types.FunctionDeclaration(
    name="get_current_month",
    description="Returns the current calendar month",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)
tool = types.Tool(
    function_declarations=[get_current_year_tool,get_current_month_tool]
)

config = types.GenerateContentConfig(
    tools=[tool]
)

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(text="What year and month is it?"),     
        ]
    )
]

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=contents,
    config=config,
)

while response.function_calls:

    tool_results = []

    for call in response.function_calls:

        print(f"Gemini requested tool call: {call.name}({call.args})")

        if call.name == "get_current_year":
            result = get_current_year()

            print("Tool Result:", result)

            tool_response = types.Part.from_function_response(
                name=call.name,
                response={"result": result}
            )

            tool_results.append(tool_response)
        
        elif call.name == "get_current_month":
            result = get_current_month()
            print("Tool Result:",result)

            tool_response = types.Part.from_function_response(
                name=call.name,
                response={"result": result},
            )
            tool_results.append(tool_response)

    contents.append(response.candidates[0].content)

    contents.append(
        types.Content(
            role="user",
            parts=tool_results
        )
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config
    )
print("Final answer :" ,response.text)
