from google.genai import types
from tools.web_tools import web_search
from tools.basic_tools import get_current_year
from tools.paper_tools import search_papers
from rag.retriever import retrieve_documents

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
paper_search_tool = types.FunctionDeclaration(
    name="search_papers",
    description="Searches OpenAlex to discover academic papers relevant to a topic. Use this when the user wants to find or discover papers.",
    parameters=types.Schema(
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
retrieve_documents_tool = types.FunctionDeclaration(
    name="retrieve_documents",
    description="Searches the locally indexed research papers in ChromaDB and returns relevant text chunks as evidence. Use this when answering questions about the content of papers already stored in the local knowledge base.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="The research question or query to search for")
        },
        required=["query"],
    )
)
tool = types.Tool(
    function_declarations=[web_search_tool,get_current_year_tool,paper_search_tool,retrieve_documents_tool]
)

config = types.GenerateContentConfig(
    tools=[tool],
    system_instruction="""
You are ScholarAI, a research assistant.

Choose tools based on the user's intent.

Tool usage:
- search_papers: discover academic papers.
- retrieve_documents: retrieve evidence from papers stored in the local knowledge base.
- web_search: retrieve current or external web information.
- get_current_year: determine the current year when needed.

When retrieve_documents is used:
- Treat its results as evidence.
- Base claims about the retrieved papers on that evidence.
- Cite retrieved evidence as [Paper Title, p. Page Number].
- If the evidence does not support an answer, say:
  "Insufficient evidence to answer this question."
- Do not invent information that is not supported by the evidence.

When multiple tools are needed, use their results together before producing the final answer.

Give a clear, concise research-oriented answer.
"""
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
        model="gemini-3.5-flash-lite",
        contents=contents,
        config=config,
    )
    tool_registry = {
        "web_search": web_search,
        "get_current_year": get_current_year,
        "search_papers":search_papers,
        "retrieve_documents":retrieve_documents,
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