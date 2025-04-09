from flask import Flask, request, jsonify
from storage import load_index, save_index, load_pages, save_pages
from searcher import do_search
from indexer import build_index
from crawler import crawl
import os

app = Flask(__name__)

INDEX_FILE = "search_index.pkl"
PAGES_FILE = "pages.pkl"
CONTENT_FILE = "seed_urls.txt"

# Load start URLs
def load_start_urls(file_path=CONTENT_FILE):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Load or build index
if os.path.exists(INDEX_FILE) and os.path.exists(PAGES_FILE):
    print("🔁 Loading index and pages from disk...")
    index, term_freqs, doc_freqs, zones = load_index(INDEX_FILE)
    pages = load_pages(PAGES_FILE)
else:
    print("🌐 Crawling and building index...")
    start_urls = load_start_urls()
    pages = crawl(start_urls)
    index, term_freqs, doc_freqs, zones = build_index(pages)
    save_index(INDEX_FILE, (index, term_freqs, doc_freqs, zones))
    save_pages(PAGES_FILE, pages)

# Snippet helper
def extract_snippet(text, query, length=200):
    query_lower = query.lower()
    text_lower = text.lower()
    index = text_lower.find(query_lower)
    if index == -1:
        return text[:length] + "..." if text else "No snippet available"
    start = max(index - 60, 0)
    end = min(index + length - 60, len(text))
    return text[start:end].strip() + "..."

# API route for Wix
@app.route('/api/search')
def api_search():
    try:
        query = request.args.get("q", "")
        zone_filter = request.args.get("zone", "all")
        page = int(request.args.get("page", 1))
        results_per_page = 10
        results = []

        if query.strip():
            raw_results = do_search(index, term_freqs, doc_freqs, zones, query)
            total_results = len(raw_results)
            start = (page - 1) * results_per_page
            end = start + results_per_page

            for url, score in raw_results[start:end]:
                body = pages.get(url, {}).get("body", "")
                snippet = extract_snippet(body, query)
                results.append({
                    "url": url,
                    "score": round(float(score), 2),
                    "snippet": snippet
                })
        else:
            total_results = 0

        return jsonify({
            "query": query,
            "page": page,
            "results": results,
            "total_results": total_results
        })

    except Exception as e:
        print("❌ Error in /api/search:", e)
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)