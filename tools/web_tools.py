from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient

client = TavilyClient()

def web_search(query: str):
    response = client.search(query=query)
    return response

if __name__ == "__main__":
    result = web_search("latest developments in retrieval augmented generation")
    print(result)

    