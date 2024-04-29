from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify
import pickle
import numpy as np
import logging
from heapq import nlargest
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def load_data():
    name = './pickle_dir/data12000_norm.pickle' #could be changed for different file in pickle_dir
    with open(name, 'rb') as file:
        sparse_matrix, all_words, urls = pickle.load(file)
    return sparse_matrix, all_words, urls


def search(query):
    sparse_matrix, all_words, urls = load_data()
    n, num_of_files = sparse_matrix.shape
    q = np.zeros(n)


    for word in query:
        if word in all_words.keys():
            q[all_words[word]] = 1

    if not (q.any() != 0):
        print("None of the words in articles")
        return []

    # normalize
    q /= np.linalg.norm(q)

    res = [(elem, i) for i, elem in enumerate(abs(q.T@sparse_matrix))]
    res = [x for x in res if x[0] > 0]
    res = nlargest(100, res, key=lambda x: x[0])
    val = []
    for elem, i in res:
        url = urls[i]
        title = url.split("/")[-1].strip()
        val.append((elem, url, title))
    return val


@app.route('/api/search', methods=['POST'])
def search_endpoint():
    query = request.json.get('query')
    logging.info(f"Search query: {query}")
    if not query:
        return jsonify({'results': []})
    
    logging.info(f"Search query: {query}")
    res = search(query)
    return jsonify({'results': res})


if __name__ == '__main__':
    app.run(debug=True)
 
