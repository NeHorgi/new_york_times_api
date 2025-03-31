from ny_times_integrate import NYTimeSource

if __name__ == "__main__":
    for batch in NYTimeSource.get_articles(batch_size=10, query="Silicon Valley"):
        for article in batch:
            article = article.get_flatten_dict(article.article_data)
            print(f" - {article['_id']} - {article['headline.main']}")
