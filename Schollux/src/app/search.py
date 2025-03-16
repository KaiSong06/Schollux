from scholarly import scholarly

def search(category, query):
    res = []
    search_results = scholarly.search_pubs(query)
    counter = 0
    if category == "topic":
        while counter < 5:
            title = next(search_results).get("bib", {}).get("title", "No title available")
            authors = next(search_results).get("bib", {}).get("author", "No authors listed")
            if title != "No title available" and authors != "No authors listed":
                res.append([title, authors])
                counter += 1
    elif category == "specific":
        while counter < 1:
            title = next(search_results).get("bib", {}).get("title", "No title available")
            authors = next(search_results).get("bib", {}).get("author", "No authors listed")
            if title != "No title available" and authors != "No authors listed":
                res.append([title, authors])
                counter += 1
    return res