def search_news(count: int):
    # Тут логіка пошуку, парсингу та вибору новин
    all_news = [
        ["Test News 1", "Description 1", "https://example.com/1"],
        ["Test News 2", "Description 2", "https://example.com/2"],
        ["Test News 3", "Description 3", "https://example.com/3"],
        ["Test News 4", "Description 4", "https://example.com/4"],
    ]
    return all_news[:count]
