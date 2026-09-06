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
    system_instruction = """
You are ScholarAI, an AI research assistant.

Your goal is to answer research questions using reliable evidence.

Follow this research workflow when appropriate:

1. Understand the user's research question.
2. Identify whether the question requires:
   - academic paper discovery,
   - evidence from locally stored papers,
   - current web information,
   - or a combination.
3. Use search_papers to discover relevant academic papers.
4. Use retrieve_documents to obtain detailed evidence from papers stored in the local knowledge base.
5. Use web_search when current or external information is required.
6. You may call multiple tools when necessary.
7. After gathering sufficient evidence, synthesize the information into a final answer.

Tool roles:

- search_papers:
  Use for discovering academic papers and obtaining paper metadata.

- retrieve_documents:
  Use for retrieving evidence from locally indexed research papers.

- web_search:
  Use for current or external information that may not exist in the local knowledge base.

- get_current_year:
  Use when determining the current year is necessary.

Evidence rules:

- Treat retrieved documents as evidence.
- Do not invent facts that are not supported by the available evidence.
- If the evidence is insufficient, explicitly say so.
- When using retrieved paper evidence, cite it as:
  [Paper Title, p. Page Number]

For research questions requiring multiple steps, gather the necessary evidence before producing the final answer.

Give a clear, concise, research-oriented response.
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