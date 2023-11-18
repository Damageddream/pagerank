import random

DAMPING = 0.85
corp = {"1.html": {"2.html"}, "2.html": {"3.html", "1.html"}, "3.html": {"2.html", "4.html"}, "4.html":{"2.html"}}
page = "1.html"
trans = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}


def transition_model(corpus, page, damping_factor):
    probability_distribution = {}
    for key in corpus:
        probability_distribution[key] = probability_distribution.get(key, 0) + (
            1 - damping_factor
        ) / len(corpus)
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
    converge_pages = 0
    while converge_pages != len(corpus):
        converge_pages = 0
        prev_rank = 0
        new_rank = 0
        for page in corpus:
            prev_rank = pagerank[page]
            sigma_pagerank_links = 0
            if(len(corpus[page])==0):
                for link in corpus:
                    sigma_pagerank_links += pagerank[link]/len(corpus)
            else:
                for link in corpus[page]:
                    sigma_pagerank_links += pagerank[link]/len(corpus[link])
            pagerank[page] = ((1-damping_factor) / len(corpus))+(damping_factor*sigma_pagerank_links)          
            new_rank = pagerank[page]
            if(abs(prev_rank - new_rank) <= 0.001):
                converge_pages += 1
    total = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] = round(pagerank[page] / total, 5)
    return pagerank

pagerank = iterate_pagerank(corp, DAMPING)
print(sum(pagerank.values()))
