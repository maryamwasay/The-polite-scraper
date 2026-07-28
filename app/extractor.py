def extract_books(soup):
    """
    Extract book information from the webpage.
    """

    books = []

    articles = soup.find_all("article", class_="product_pod")

    for article in articles:

        title = article.h3.a["title"]

        price = article.find("p", class_="price_color").text

        rating = article.p["class"][1]

        availability = article.find_all("p")[1].text.strip()

        url = article.h3.a["href"]

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": url
        })

    return books
