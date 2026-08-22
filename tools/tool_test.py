from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from tools.web_tools import web_search

client = genai.Client()

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
tool = types.Tool(
    function_declarations=[web_search_tool]
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

    while response.function_calls:
        tool_results=[]

        for call in response.function_calls:
            print(f"Gemini requested tool call: {call.name}({call.args})")

            if call.name == "web_search":
                query = call.args["query"]
                result = web_search(query)

                print("Tool Result:" , result)

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
            model="gemini-3.6-flash",
            contents=contents,
            config=config,
        )
    return response.text

question = "What are the latest developments in Retrieval-Augmented Generation?"

answer = research(client, question)

print("Final answer:", answer)