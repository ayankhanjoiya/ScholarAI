from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient

client = TavilyClient()

def web_search(query: str):
    response = client.search(query=query)

    results = []
    for result in response[results]:
        result.append({
            "title":result.title,
            "url":result.url,
            "content":result.content
        })
    return results

    