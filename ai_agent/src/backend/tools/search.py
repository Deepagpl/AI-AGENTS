from typing import Dict, List
from duckduckgo_search import DDGS

class SearchTool:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform a web search using DuckDuckGo.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of search results with title, link, and snippet
        """
        try:
            results = []
            for r in self.ddgs.text(query, max_results=max_results):
                print(f"Raw result: {r}")  # Debug print
                try:
                    result = {
                        'title': r.get('title', 'No title'),
                        'link': r.get('href', 'No link'),  # Changed from 'link' to 'href'
                        'snippet': r.get('body', 'No snippet')
                    }
                    results.append(result)
                except Exception as e:
                    print(f"Error processing search result: {str(e)}")
            return results
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return [{'error': f'Search failed: {str(e)}'}]

    def format_results(self, results: List[Dict]) -> str:
        """
        Format search results into a readable string.
        
        Args:
            results (List[Dict]): List of search results
            
        Returns:
            str: Formatted string of search results
        """
        if not results:
            return "No results found."
            
        formatted = []
        for i, result in enumerate(results, 1):
            if 'error' in result:
                return f"Error: {result['error']}"
                
            formatted.append(f"{i}. {result['title']}")
            formatted.append(f"   Link: {result['link']}")
            formatted.append(f"   {result['snippet']}\n")
            
        return "\n".join(formatted)

    async def async_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Async version of search method for concurrent operations.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of search results
        """
        # In a real async implementation, we would use aiohttp or similar
        # For now, we'll just call the sync version
        return self.search(query, max_results)
