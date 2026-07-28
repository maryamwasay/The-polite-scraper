from bs4 import BeautifulSoup


def parse_html(html):
    """
    Converts raw HTML into BeautifulSoup object.
    """

    soup = BeautifulSoup(html, "lxml")

    return soup
