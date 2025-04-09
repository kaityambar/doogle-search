import pickle

def save_index(filename, index_data):
    with open(filename, 'wb') as f:
        pickle.dump(index_data, f)

def load_index(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save_pages(filename, pages):
    with open(filename, 'wb') as f:
        pickle.dump(pages, f)

def load_pages(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
