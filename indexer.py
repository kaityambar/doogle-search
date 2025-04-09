import re
from collections import defaultdict
from stopwords import stopwords

# 💡 Replace lambdas with named functions so pickle works
def default_list_dict():
    return defaultdict(list)

def default_int_dict():
    return defaultdict(int)

def default_zone_dict():
    return defaultdict(set)

def build_index(pages):
    index = defaultdict(default_list_dict)     # word → {url: [positions]}
    term_freqs = defaultdict(default_int_dict) # url → {word: frequency}
    doc_freqs = defaultdict(int)               # word → # of documents with it
    zones = defaultdict(default_zone_dict)     # word → {'title': {url}, 'headings': {url}}

    for url, content in pages.items():
        title = content['title']
        headings = content['headings']
        body = content['body']

        # Tokenize body for position-based indexing
        words = re.findall(r'\w+', body.lower())
        seen = set()

        for position, word in enumerate(words):
            if word in stopwords:
                continue
            index[word][url].append(position)
            term_freqs[url][word] += 1
            if word not in seen:
                doc_freqs[word] += 1
                seen.add(word)

        # Handle boosting zones
        for word in re.findall(r'\w+', title.lower()):
            if word not in stopwords:
                zones[word]['title'].add(url)

        for word in re.findall(r'\w+', headings.lower()):
            if word not in stopwords:
                zones[word]['headings'].add(url)

    return index, term_freqs, doc_freqs, zones
