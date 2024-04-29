import pickle
import numpy as np
import time


def load_data(name):
    with open(f'./pickle_dir/{name}', 'rb') as file:
        sparse_matrix, all_words, urls = pickle.load(file)
    return sparse_matrix, all_words, urls


def search(query, name):
    sparse_matrix, all_words, urls = load_data(name)

    n, num_of_files = sparse_matrix.shape
    print(f"Num of files: {num_of_files}")
    q = np.zeros(n)

    for word in query:
        if word in all_words.keys():
            q[all_words[word]] = 1

    if not (q.any() != 0):
        print("None of the words in articles")
        return

    # normalize
    q /= np.linalg.norm(q)

    res = [(elem, i) for i, elem in enumerate(abs(q.T @ sparse_matrix))]

    res.sort(reverse=True)
    tab_of_urls = [urls[url_idx] for elem, url_idx in res if elem > 0]
    return res, tab_of_urls, n


if __name__ == '__main__':
    query = ["internet", "python", "web"]
    tab = [100, 500, 700, 850, 990]
    print("----------   No SVD   ----------")
    t1 = time.time()
    res, urls, n = search(query, f"data1000_without_norm.pickle")
    t2 = time.time()
    print(f"Time :{t2 - t1}")
    print("Correlations:")
    print([x for x, _ in res[:5]])
    print(urls[:5])
    print(f"Words in dictionary: {n}")
    for k in tab:
        print(f"---------- SVD: k={k} ----------")
        t1 = time.time()
        res, urls, n = search(query, f"data1000_SVD_k{k}.pickle")
        t2 = time.time()
        print(f"Time :{t2 - t1}")
        print("Correlations:")
        print([x for x, _ in res[:5]])
        print(urls[:5])
        print(f"Words in dictionary: {n}")
