from datetime import datetime
from datetime import date
import csv

import requests
import pandas as pd
import urllib.parse
import matplotlib.pyplot as plt
import seaborn as sns

API = "https://incubator.wikimedia.org/w/rest.php/v1/"
HEADERS = {
    "User-Agent": "Arcstur Scripts (https://meta.wikimedia.org/wiki/User:Arcstur)",
}

# TODO: obter essa lista automaticamente
# obtido de <https://incubator.wikimedia.org/wiki/Special:PrefixIndex?prefix=Wp%2Fkgp%2F&namespace=0&hideredirects=1>
titles = [
    "Wp/kgp/'Ó To Vẽme",
    "Wp/kgp/500 Prỹg",
    "Wp/kgp/Acento gráfico fóg vĩ ki, kar Kanhgág vĩ ki",
    "Wp/kgp/Brasil",
    "Wp/kgp/Brincadeira corrida do saco( Morsa kãkã jẽ kỹ, vẽnhvó)",
    "Wp/kgp/Dentro e fora ( Kãki, pãtã sỹn)",
    "Wp/kgp/Farĩnh totor",
    "Wp/kgp/Fua tu vẽme",
    "Wp/kgp/Fuva",
    "Wp/kgp/Fuva to vẽme",
    "Wp/kgp/FÁG-TO VÃME",
    "Wp/kgp/Fág",
    "Wp/kgp/Fág-Nhin",
    "Wp/kgp/Fág tynyr",
    "Wp/kgp/Fág tỹ kyfe",
    "Wp/kgp/Fãfãn Vãme",
    "Wp/kgp/Fójin Vãme",
    "Wp/kgp/Fẽfẽn",
    "Wp/kgp/Fỹj",
    "Wp/kgp/Gangao",
    "Wp/kgp/Gangao vẽme",
    "Wp/kgp/Gangavo",
    "Wp/kgp/Garĩnh nug",
    "Wp/kgp/Garĩnh nĩsóg",
    "Wp/kgp/Garĩnh ta fór",
    "Wp/kgp/Go or",
    "Wp/kgp/Goj tu vẽme",
    "Wp/kgp/Goj tu vẽmẽ",
    "Wp/kgp/Gren",
    "Wp/kgp/Gren to vẽme",
    "Wp/kgp/Grun",
    "Wp/kgp/Grũ",
    "Wp/kgp/Gufã",
    "Wp/kgp/Gãr kuka tu vãme",
    "Wp/kgp/Gãr ránrár",
    "Wp/kgp/Gãr ránrár tu vãme",
    "Wp/kgp/Gãr ránrár tỹ ẽmĩ",
    "Wp/kgp/Gónvẽ Vãme",
    "Wp/kgp/Gĩr kar kyrũ sĩ kar kyrũ",
    "Wp/kgp/Hẽrig tu vãme",
    "Wp/kgp/Inh jamré fag",
    "Wp/kgp/Jóhó",
    "Wp/kgp/KUSÃGKE RĨR",
    "Wp/kgp/Ka tỹ gatu to pẽg",
    "Wp/kgp/Kajér",
    "Wp/kgp/Kajẽr tỹ mĩg mré vẽnh génh kãme",
    "Wp/kgp/Kanhgang jyjy",
    "Wp/kgp/Kanhgág Vẽnhkagta",
    "Wp/kgp/Kanhgág vĩ ki jyjy pẽ",
    "Wp/kgp/Kanhgág ãg kanhrãn fã pẽ",
    "Wp/kgp/Kanhgág ũ tỹ ne né",
    "Wp/kgp/Kanhkã tá ti nĩ",
    "Wp/kgp/Kanẽ sĩ tavĩ",
    "Wp/kgp/Kanẽsã to vẽme",
    "Wp/kgp/Kapẽn tu vãme",
    "Wp/kgp/Karugmág",
    "Wp/kgp/Kasor to vême",
    "Wp/kgp/Ketyjug tu vãme",
    "Wp/kgp/Ko vãnh ũ ti garĩnh nér",
    "Wp/kgp/Kri nĩj fã pénĩn vẽnhgrén",
    "Wp/kgp/Kréj",
    "Wp/kgp/Krĩg sĩnvĩ",
    "Wp/kgp/Kukrej",
    "Wp/kgp/Kumi",
    "Wp/kgp/Kãj",
    "Wp/kgp/Kãme kar Pénĩ",
    "Wp/kgp/Kó'y Vãme",
    "Wp/kgp/Kóhon",
    "Wp/kgp/Main Page",
    "Wp/kgp/Momro",
    "Wp/kgp/Mĩg Vãme",
    "Wp/kgp/NO",
    "Wp/kgp/Ninsu",
    "Wp/kgp/No kar vyj to vãme",
    "Wp/kgp/Nãn ga",
    "Wp/kgp/Nẽnkanh mré Nẽnẽ tu vãme",
    "Wp/kgp/Nẽnẽ to Vẽme",
    "Wp/kgp/Pego pego ( inh kâgmira, inh kâgmira)",
    "Wp/kgp/Pirã",
    "Wp/kgp/Pisé",
    "Wp/kgp/Pãi ag to vãme",
    "Wp/kgp/Pãri",
    "Wp/kgp/Pãtá sỹm ke",
    "Wp/kgp/Pého féj",
    "Wp/kgp/Pénfág",
    "Wp/kgp/Pénĩ",
    "Wp/kgp/Pépo pẽn kókré",
    "Wp/kgp/Pó tãpér tỹ vẽnh kanhir",
    "Wp/kgp/Pẽnturó",
    "Wp/kgp/Pẽnva",
    "Wp/kgp/Pỹn",
    "Wp/kgp/Rarỹnh Pãn",
    "Wp/kgp/Rarỹnh kãme",
    "Wp/kgp/Rijero ga",
    "Wp/kgp/Rã",
    "Wp/kgp/Seraj",
    "Wp/kgp/Sukrĩg",
    "Wp/kgp/Sukrĩg jógo",
    "Wp/kgp/Sãpe to vẽme",
    "Wp/kgp/To Vãme sĩ",
    "Wp/kgp/To vãme",
    "Wp/kgp/Tupẽ tỹ ẽg mré nĩn kỹ",
    "Wp/kgp/Tusĩnh Tỹ mỹg pẽfyn",
    "Wp/kgp/Van to vẽme",
    "Wp/kgp/Voga",
    "Wp/kgp/VÊNHPRŨG",
    "Wp/kgp/Vãfy téj(tuja)balaio de tampa",
    "Wp/kgp/Vãfy vãme",
    "Wp/kgp/Vãnh Kãmĩ Grugru",
    "Wp/kgp/Vãrensĩn",
    "Wp/kgp/Vẽnh prũg to vãme",
    "Wp/kgp/Vẽnhkagta",
    "Wp/kgp/Vẽser to vẽme",
    "Wp/kgp/Wp/kgp/",
    "Wp/kgp/kumĩ",
    "Wp/kgp/mỹnjóka",
    "Wp/kgp/Ãma kãmĩ kanhgág jykre pẽ tu ke .",
    "Wp/kgp/Ó",
    "Wp/kgp/ẼMĨ",
    "Wp/kgp/Ẽg Kygtãg",
    "Wp/kgp/Ẽg rá",
    "Wp/kgp/Ẽg vĩ ki alfabeto",
    "Wp/kgp/Ẽkór tỹ ẽmῖ",
    "Wp/kgp/Ẽmro",
    "Wp/kgp/Ẽmã Ketyjug Tẽgtũ tu vãme sĩ",
    "Wp/kgp/Ẽmã tỹ Karugmág vẽnh han kãme",
]


def main():
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


def get_first_revision(title):
    escaped_title = urllib.parse.quote(title, safe="")
    res = requests.get(API + "page/" + escaped_title + "/history", headers=HEADERS)
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
    writer = csv.writer(csvfile)
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
