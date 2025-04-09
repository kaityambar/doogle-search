import math

def compute_scores(index, term_freqs, doc_freqs, zones, query, total_docs):
    query_words = query.lower().split()
    scores = {}

    for word in query_words:
        if word not in index:
            continue

        # IDF with smoothing
        df = doc_freqs.get(word, 0)
        idf = math.log((total_docs + 1) / (1 + df))

        for url in index[word]:
            tf = term_freqs.get(url, {}).get(word, 0)
            score = tf * idf

            # Zone-based Boosting
            word_zones = zones.get(word, {})
            if url in word_zones.get('title', set()):
                score *= 2.0
            elif url in word_zones.get('headings', set()):
                score *= 1.5

            scores[url] = scores.get(url, 0.0) + float(score)

    # Return sorted results by score
    return sorted(
        [(url, float(score)) for url, score in scores.items()],
        key=lambda x: x[1],
        reverse=True
    )

def do_search(index, term_freqs, doc_freqs, zones, query):
    total_docs = len(term_freqs)
    return compute_scores(index, term_freqs, doc_freqs, zones, query, total_docs)
