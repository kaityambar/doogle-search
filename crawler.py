import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(start_urls, max_pages=5):
    visited = set()
    to_visit = list(start_urls)
    pages = {}

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()
        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract parts of the page
            title = soup.title.string.strip() if soup.title else ""
            headings = " ".join(h.get_text(strip=True) for h in soup.find_all(['h1', 'h2']))
            body = soup.get_text(separator=' ', strip=True)

            pages[current_url] = {
                'title': title,
                'headings': headings,
                'body': body
            }

            visited.add(current_url)

            # Add new links to crawl
            for link in soup.find_all('a', href=True):
                full_url = urljoin(current_url, link['href'])
                if full_url.startswith("http") and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return pages
