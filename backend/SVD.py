import pickle

import numpy as np
from scipy.sparse.linalg import svds
from sklearn.decomposition import TruncatedSVD
from sklearn. preprocessing import normalize


def load_data():
    with open('./pickle_dir/data1000_without_norm.pickle', 'rb') as file:
        sparse_matrix, all_words, urls = pickle.load(file)
    return sparse_matrix, all_words, urls


def execute_SVD(k):
    sparse_matrix, all_words, urls = load_data()
    U, Sigma, VT = svds(sparse_matrix, k=k)

    rare_matrix = np.dot(U, np.dot(np.diag(Sigma), VT))
    sparse_matrix = normalize(rare_matrix, axis=0, norm='l2')

    with open(f'./pickle_dir/data1000_SVD_k{k}.pickle', 'wb') as file:
        pickle.dump((sparse_matrix, all_words, urls), file)


if __name__ == '__main__':
    execute_SVD(990)
