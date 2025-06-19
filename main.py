import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag

visited = set()

def crawl(url, depth=2):
    if depth == 0 or url in visited:
        return
    print(f"Visiting: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        if "text/html" not in response.headers.get("Content-Type", ""):
            return
        soup = BeautifulSoup(response.text, "html.parser")
        for link_tag in soup.find_all("a", href=True):
            href = link_tag['href']
            next_url = urldefrag(urljoin(url, href)).url
            if urlparse(next_url).netloc == urlparse(url).netloc:
                crawl(next_url, depth - 1)
    except Exception as e:
        print(f"Error crawling {url}: {e}")

crawl("https://www.naver.com")