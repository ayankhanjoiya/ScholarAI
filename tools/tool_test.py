from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from tools.web_tools import web_search
from tools.basic_tools import get_current_year

client = genai.Client()
from google.genai import types
from tools.web_tools import web_search
from tools.basic_tools import get_current_year
from tools.paper_tools import search_papers
from rag.retriever import retrieve_documents
from agents.researcher import research

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
    description="Searches for relevant academic papers and returns their title, publication year, DOI, and paper ID.",
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
    description="Searches the locally stored research papers for relevant evidence and returns the paper title, page number, paper ID, and content.",
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
    tools=[tool]
)

question = "According to the BERT paper, how does masked language modeling work?"

answer = research(client, question)

print("Final answer:", answer)