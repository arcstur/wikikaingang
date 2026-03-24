# dependencies = [
#   "requests",
# ]

import requests
import urllib.parse
from bs4 import BeautifulSoup

API = "https://incubator.wikimedia.org/w/rest.php/v1/"
USER_AGENT = "Arcstur Scripts (https://meta.wikimedia.org/wiki/User:Arcstur)"
ARTICLES_URL = "https://incubator.wikimedia.org/wiki/Special:PrefixIndex?prefix=Wp%2Fkgp%2F&namespace=0&hideredirects=1"


def main():
    titles = get_titles()
    titles_without_cat = []
    for title in titles:
        print(f"{title}...")
        content = get_content(title)
        if "Category:Wp/kgp" not in content:
            titles_without_cat.append(title)

    print()
    if titles_without_cat:
        print("Title without Wp/kgp category:")
        print()
        for title in titles_without_cat:
            escaped_title = urllib.parse.quote(title, safe="")
            print(f"https://incubator.wikimedia.org/wiki/{escaped_title}")
    else:
        print("YAY! All mainspace articles have the control category.")


def get_content(title):
    escaped_title = urllib.parse.quote(title, safe="")
    res = requests.get(
        API + "page/" + escaped_title,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    res.raise_for_status()
    data = res.json()
    return data["source"]


def get_titles():
    print(f"Making request to {ARTICLES_URL}...")
    res = requests.get(
        ARTICLES_URL, headers={"User-Agent": USER_AGENT, "Accept": "text/html"}
    )
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    titles = []
    anchors = soup.find("ul", class_="mw-prefixindex-list").find_all("a")
    for a in anchors:
        titles.append(a["title"])
    return titles


if __name__ == "__main__":
    main()
