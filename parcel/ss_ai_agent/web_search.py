import requests

class WebSearchService:
    def __init__(self):
        pass

    def search(self, query: str) -> str:
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                return f"Web search completed for: {query}. (HTML content length: {len(res.text)})"
            return f"Web search status code: {res.status_code}"
        except Exception as e:
            return f"Web search error: {str(e)}"

    def fetch_url(self, target_url: str) -> str:
        try:
            import trafilatura
            downloaded = trafilatura.fetch_url(target_url)
            text = trafilatura.extract(downloaded)
            return text or "Could not extract main content from URL."
        except Exception:
            try:
                res = requests.get(target_url, timeout=5)
                return res.text[:5000]
            except Exception as e:
                return f"Fetch URL error: {str(e)}"
