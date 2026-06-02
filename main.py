from src.tools.tools import web_search, scrape_url

# output = web_search("Latest news on AI research")
# print(output)

# results = scrape_url("https://www.artificialintelligence-news.com/")
# print(results)

result = web_search.invoke("What is the latest research on using AI for climate change mitigation?")
print(result)