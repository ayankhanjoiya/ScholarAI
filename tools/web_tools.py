from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient

client = TavilyClient()

def web_search(query: str):
    response = client.search(query=query)

    search_results = []
    for result in response["results"]:
        search_results.append({
            "title":result["title"],
            "url":result["url"],
            "content":result["content"]
        })
    return search_results