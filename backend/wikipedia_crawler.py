import pickle
from collections import Counter
import numpy as np
import wikipedia
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import time
from scipy.sparse import csr_matrix
from sklearn. preprocessing import normalize

# nltk.download('punkt')

language = 'en'
stop_words = set(stopwords.words('english'))


def fetch_article_links(start_page, max_articles):
    article_links = set()
    article_links.add(wikipedia.page(start_page).url)
    visited_links = set()

    while len(article_links) < max_articles:
        current_link = article_links.pop()
        if current_link in visited_links:
            continue
        visited_links.add(current_link)

        try:
            response = requests.get(current_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                link_href = link['href']
                if link_href.startswith('/wiki/') and ':' not in link_href:
                    article_links.add('https://en.wikipedia.org' + link_href)

        except:
            pass
        time.sleep(0.5)
    return list(article_links)[:max_articles]


def fetch_article_content(article_links):
    articles = []
    for link in article_links:
        try:
            print(f"Fetching article: {link}")
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            tokens = word_tokenize(text)
            tokens = [word.lower() for word in tokens]
            stop_words = set(stopwords.words('english'))
            tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
            cnt = Counter(tokens).most_common(150)
            content = [item for item, _ in cnt]
            articles.append((link, content, cnt))
        except:
            print(1)
            pass

    with open("list_of_links_12000_norm.txt", "w") as file:
        for item in articles:
            line = ';'.join(map(str, item))
            file.write(line + '\n')
    return articles


def remove_stopwords(article):
    article = re.sub(r'[^\w\s]', '', article).lower()
    tokens = word_tokenize(article)
    filtered_article = [word for word in tokens if word not in stop_words]
    filtered_article = ' '.join(filtered_article)

    return filtered_article


def save_articles(articles):
    all_words = dict()
    num_of_files = len(articles)
    nm = Counter()
    bags = []
    idx = 0
    urls = dict()

    for i, (url, content, cnt) in enumerate(articles):
        bags.append(cnt)
        nm.update(Counter(content))
        urls[i] = url
        for word in content:
            if word not in all_words:
                all_words[word] = idx
                idx += 1
        print(f"Article num: {i+1}")

    n = len(all_words)

    word_count = np.array([])
    rows_idx = np.array([])
    cols_idx = np.array([])

    for i in range(num_of_files):
        for elem, count in bags[i]:
            word_count = np.append(word_count, count * np.log(num_of_files / nm[elem]))
            rows_idx = np.append(rows_idx, all_words[elem])
            cols_idx = np.append(cols_idx, i)

    sparse_matrix = csr_matrix((word_count, (rows_idx, cols_idx)), shape=(n, num_of_files))

    # normalize
    sparse_matrix_csr = sparse_matrix.tocsr()
    column_norms = np.sqrt((sparse_matrix_csr.power(2)).sum(axis=0))
    column_norms[column_norms == 0] = 1
    sparse_matrix = sparse_matrix_csr / column_norms

    with open('./pickle_dir/data12000_norm.pickle', 'wb') as file:
        pickle.dump((sparse_matrix, all_words, urls), file)


def main():
    start_page = 'Earth'
    max_articles = 12000

    article_links = fetch_article_links(start_page, max_articles)
    print(article_links)

    articles = fetch_article_content(article_links)

    save_articles(articles)


if __name__ == "__main__":
    main()
