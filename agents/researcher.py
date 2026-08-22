from google.genai import types
from tools.web_tools import web_search
from tools.basic_tools import get_current_year

web_search_tool = types.FunctionDeclaration(
    name = "web_search",
    description = "Searches the web and returns relevant search results for a given query.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type = types.Type.STRING,
                description = "The search query to use"
            )
        },
        required=["query"],
    )
)
get_current_year_tool = types.FunctionDeclaration(
    name = "get_current_year",
    description = "gives us the current year",
    parameters={},
)
tool = types.Tool(
    function_declarations=[web_search_tool,get_current_year_tool]
)

config = types.GenerateContentConfig(
    tools=[tool]
)

def research(client,question):
    contents =[
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question),
            ]
        )
    ]
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config,
    )
    tool_registry = {
        "web_search": web_search,
        "get_current_year": get_current_year,
    }
    while response.function_calls:
        tool_results=[]

        for call in response.function_calls:
            print(f"Gemini requested tool call: {call.name}({call.args})")

            tool_function = tool_registry[call.name]
            result = tool_function(**call.args)

            print("Tool Result: " ,result)

            tool_response = types.Part.from_function_response(
                name=call.name,
                response={"result":result}
            )
            tool_results.append(tool_response)
        
        contents.append(response.candidates[0].content)

        contents.append(
            types.Content(
                role="user",
                parts=tool_results,
            )
        )
        
        response=client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents,
            config=config,
        )
    return response.text