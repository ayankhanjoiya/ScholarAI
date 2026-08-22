import requests


def search_papers(query: str):

    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": 5
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    papers = []

    for paper in data["results"]:

        papers.append({
            "paper_id": paper["id"],
            "title": paper["title"],
            "year": paper["publication_year"],
            "doi": paper["doi"],
        })

    return papers


def get_paper(paper_id: str):

    response = requests.get(paper_id)

    paper = response.json()

    return {
        "paper_id": paper["id"],
        "title": paper["title"],
        "year": paper["publication_year"],
        "doi": paper["doi"],
        "abstract": paper["abstract_inverted_index"],
    }