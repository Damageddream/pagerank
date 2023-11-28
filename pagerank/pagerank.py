import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    probability_distribution = {}
    for key in corpus:
        probability_distribution[key] = probability_distribution.get(key, 0) + (1 - damping_factor) / len(corpus)
        if len(corpus[page]) == 0:
            probability_distribution[key] += damping_factor / len(corpus)
        elif key == page:
            for page_key in corpus[key]:
                probability_distribution[page_key] = probability_distribution.get(
                    page_key, 0
                ) + damping_factor / len(corpus[key])
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    pagerank = {}
    page = random.choice(list(corpus.keys()))
    for i in range(n):
        pagerank[page] = pagerank.get(page, 0) + 1
        transition = transition_model(corpus, page, damping_factor)
        page = random.choices(list(transition.keys()), weights=list(transition.values()), k=1)[0]

    for key in pagerank:
        pagerank[key] = pagerank[key] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    while True:
        converge_pages = 0
        prev_rank = 0
        new_rank = 0
        for page in corpus:
            prev_rank = pagerank[page]
            sigma_pagerank_links = 0
            for link in corpus:
                if len(corpus[link]) == 0:
                    sigma_pagerank_links += pagerank[link] / len(corpus)
                elif page in corpus[link]:
                    sigma_pagerank_links += pagerank[link] / len(corpus[link])
            pagerank[page] = ((1-damping_factor) / len(corpus))+(damping_factor*sigma_pagerank_links)          
            new_rank = pagerank[page]
            if(abs(prev_rank - new_rank) <= 0.001):
                converge_pages += 1
        if converge_pages == len(corpus):
            break
    total = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] = round(pagerank[page] / total, 5)
    return pagerank

if __name__ == "__main__":
    main()