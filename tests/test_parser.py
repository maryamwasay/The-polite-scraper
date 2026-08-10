from app.parser import (
    parse_catalogue_links,
    parse_next_page,
)


def test_relative_links_become_absolute():

    html = """
    <html>
        <body>
            <article class="product_pod">
                <h3>
                    <a href="../book/test_1/index.html">
                        Test Book
                    </a>
                </h3>
            </article>
        </body>
    </html>
    """

    links = parse_catalogue_links(
        html,
        "https://books.toscrape.com/catalogue/page-1.html",
    )

    assert len(links) == 1

    assert links[0].startswith(
        "https://books.toscrape.com/"
    )


def test_duplicate_links_are_removed():

    html = """
    <article class="product_pod">
        <h3>
            <a href="../book/test/index.html">
                Test
            </a>
        </h3>
    </article>

    <article class="product_pod">
        <h3>
            <a href="../book/test/index.html">
                Test
            </a>
        </h3>
    </article>
    """

    links = parse_catalogue_links(
        html,
        "https://books.toscrape.com/catalogue/page-1.html",
    )

    assert len(links) == 1


def test_next_page():

    html = """
    <ul class="pager">
        <li class="next">
            <a href="page-2.html">
                next
            </a>
        </li>
    </ul>
    """

    next_url = parse_next_page(
        html,
        "https://books.toscrape.com/catalogue/page-1.html",
    )

    assert (
        next_url
        == "https://books.toscrape.com/catalogue/page-2.html"
    )


def test_no_next_page():

    html = """
    <ul class="pager"></ul>
    """

    next_url = parse_next_page(
        html,
        "https://books.toscrape.com/catalogue/page-3.html",
    )

    assert next_url is None