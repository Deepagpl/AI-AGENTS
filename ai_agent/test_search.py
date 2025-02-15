import asyncio
from src.backend.tools.search import SearchTool

async def test_search():
    search_tool = SearchTool()
    query = "What is the capital of France?"
    results = await search_tool.async_search(query)
    print(f"Search query: {query}")
    print("Raw results:")
    print(results)
    formatted_results = search_tool.format_results(results)
    print("Formatted results:")
    print(formatted_results)

if __name__ == "__main__":
    asyncio.run(test_search())
