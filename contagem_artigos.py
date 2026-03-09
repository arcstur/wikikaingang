# dependencies = [
#   "requests",
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "beautifulsoup4",
# ]

from datetime import datetime
from datetime import date
from bs4 import BeautifulSoup
import csv

import requests
import pandas as pd
import urllib.parse
import matplotlib.pyplot as plt
import seaborn as sns

API = "https://incubator.wikimedia.org/w/rest.php/v1/"
USER_AGENT = "Arcstur Scripts (https://meta.wikimedia.org/wiki/User:Arcstur)"
ARTICLES_URL = "https://incubator.wikimedia.org/wiki/Special:PrefixIndex?prefix=Wp%2Fkgp%2F&namespace=0&hideredirects=1"


def main():
    titles = get_titles()
    title_to_revision = {}
    for title in titles:
        print(f"{title}...")
        first = get_first_revision(title)
        title_to_revision[title] = first
    timestamps = [r["timestamp"] for r in title_to_revision.values()]
    counts = count_items_per_month(timestamps)
    print(counts)
    plot_item_counts(counts)

    with open("artigos.csv", "w") as f:
        export_articles(title_to_revision, f)


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


def get_first_revision(title):
    escaped_title = urllib.parse.quote(title, safe="")
    res = requests.get(
        API + "page/" + escaped_title + "/history",
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    res.raise_for_status()
    data = res.json()
    first = data["revisions"][-1]
    assert first["delta"] is None
    return first


def count_items_per_month(timestamps):
    # Parse timestamps
    dates = [datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ") for t in timestamps]

    df = pd.DataFrame({"date": dates})

    # Filter from start month (inclusive)
    start = pd.Period("2025-10", freq="M")
    df["month"] = df["date"].dt.to_period("M")
    df.loc[df["month"] < start, "month"] = start

    # Count per month
    monthly_counts = (
        df.groupby("month")["date"].count().sort_index().reset_index(name="item_count")
    )

    # Cumulative count
    monthly_counts["count"] = monthly_counts["item_count"].cumsum()

    return monthly_counts[["month", "count"]]


def plot_item_counts(item_counts):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="month", y="count", data=item_counts)
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=3)
    plt.xticks(rotation=45)
    plt.xlabel("Mês")
    plt.ylabel("Artigos")
    plt.title(f"Wikikaingáng: quantidade total de artigos na incubadora {date.today()}")
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.savefig("artigos.png", dpi=300, bbox_inches="tight")


def export_articles(title_to_revision, csvfile):
    print("Exporting csv...")
    writer = csv.writer(csvfile, delimiter="\t")
    writer.writerow(
        [
            "artigo",
            "link",
            "usuário",
            "data",
        ]
    )
    for title, revision in title_to_revision.items():
        writer.writerow(
            [
                title,
                "https://incubator.wikimedia.org/wiki/" + urllib.parse.quote(title),
                revision["user"]["name"],
                revision["timestamp"],
            ]
        )


if __name__ == "__main__":
    main()
