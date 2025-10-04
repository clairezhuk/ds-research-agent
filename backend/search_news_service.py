import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# List of RSS sources
RSS_FEEDS = [
    "https://www.technologyreview.com/feed/",
    "https://export.arxiv.org/rss/cs.LG",
    "https://export.arxiv.org/rss/cs.AI",
    "https://ai.googleblog.com/feeds/posts/default",
    "https://deepmind.com/blog/feed/basic/",
    "https://ai.meta.com/blog/rss/",
    "https://blogs.nvidia.com/feed/",
    "https://openai.com/blog/rss.xml"
]

def fetch_rss_articles(feeds, max_items=10):
    articles = []
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_items]:
                article = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", "")
                }
                articles.append(article)
        except Exception as e:
            print(f"Error parsing {feed_url}: {e}")
    return articles


# --- Simple search for most relevant ---
def simple_rank_articles(query, dataframe, top_k=5):
    # Use TF-IDF on summary + title
    corpus = (dataframe["title"] + ". " + dataframe["summary"]).tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Query vector
    query_vec = vectorizer.transform([query])
    
    # Cosine similarity
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Add to DataFrame and sort
    dataframe["score"] = sim_scores
    return dataframe.sort_values(by="score", ascending=False).head(top_k)


def search_news(count: int):
    articles = fetch_rss_articles(RSS_FEEDS, max_items=10)
    df = pd.DataFrame(articles)
    df.to_csv("news_dataset.csv", index=False, encoding="utf-8")
    query = "latest developments in AI and machine learning"
    top_articles = simple_rank_articles(query, df, top_k=5)
    result = [
        [row["title"], row["published"], row["link"] ]
        for _, row in top_articles.iterrows()
    ]
    return result
