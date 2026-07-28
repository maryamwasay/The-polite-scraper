def clean_books(books):
    """
    Cleans extracted book data.
    """

    cleaned = []

    for book in books:

        price = book["price"].replace("£", "")

        cleaned.append({
            "title": book["title"].strip(),
            "price": price,
            "rating": book["rating"],
            "availability": book["availability"],
            "url": book["url"]
        })

    return cleaned
