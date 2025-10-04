import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import pipeline
from newspaper import Article

# ---------------------------
# 1. Функція пошуку (Google News через RSS)
# ---------------------------
def fetch_news_rss(query="data science", num_results=10):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item")[:num_results]

    news = []
    for item in items:
        title = item.title.text
        # спочатку беремо origLink, якщо є
        orig_link = item.find("link").text
        if item.find("guid"):
            orig_link = item.find("guid").text
        if item.find("feedburner:origLink"):
            orig_link = item.find("feedburner:origLink").text

        news.append({"title": title, "link": orig_link})
    return news


# ---------------------------
# 2. Завантаження тексту статті
# ---------------------------
def fetch_text_from_url(url, max_paragraphs=20, debug=False):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/127.0.0.0 Safari/537.36"
            )
        }

        # перший запит — google news redirect
        resp = requests.get(url, timeout=10, allow_redirects=True, headers=headers)
        
        final_url = resp.url
        if debug:
            print("Final URL:", final_url)

        # якщо ми досі на google.com → реального посилання нема
        if "google.com" in final_url:
            if debug:
                print("Still on google.com, no redirect happened.")
            return ""

        # тепер качаємо вже реальну сторінку
        resp2 = requests.get(final_url, timeout=10, headers=headers)
        soup = BeautifulSoup(resp2.text, "html.parser")

        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            print("Newspaper3k error:", e)
            return ""

    except Exception as e:
        if debug:
            print("Error:", e)
        return ""


# ---------------------------
# 3. Створюємо датасет
# ---------------------------
def build_dataset(query="data science", num_results=10):
    news = fetch_news_rss(query, num_results)
    for n in news:
        n["text"] = fetch_text_from_url(n["link"])
    df = pd.DataFrame(news)
    return df

# ---------------------------
# 4. Summarization через BART
# ---------------------------
def summarize_texts(texts, model_name="facebook/bart-large-cnn", max_length=100, min_length=30):
    summarizer = pipeline("summarization", model=model_name)
    summaries = []
    for t in texts:
        if len(t) < 500:  # занадто коротке для summary
            summaries.append(t[:200])
        else:
            summary = summarizer(t, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(summary[0]["summary_text"])
    return summaries

# ---------------------------
# 5. Демонстрація
# ---------------------------
if __name__ == "__main__":
    df = build_dataset("data science machine learning", num_results=5)
    print("Завантажено статей:", len(df))
    
    df["summary"] = summarize_texts(df["text"].tolist())
    df.to_csv("news_dataset.csv", index=False)

    print(df[["title", "summary", "link"]])
