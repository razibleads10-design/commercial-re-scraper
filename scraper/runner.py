
import argparse
from pathlib import Path

import pandas as pd

from scraper.scraper import PropertyScraper


ROOT = Path(__file__).resolve().parent.parent

COLUMNS = [
    "title",
    "price",
    "location",
    "broker",
    "phone",
    "url"
]


def save_results(records, output_file):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(records, columns=COLUMNS)

    dataframe.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Listings exported: {len(dataframe)}")
    print(f"File: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Commercial property listing scraper"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Starting directory URL"
    )

    parser.add_argument(
        "--pages",
        type=int,
        default=5
    )

    parser.add_argument(
        "--output",
        default="data/sample_listings.csv"
    )

    args = parser.parse_args()

    if args.pages < 1:
        parser.error("--pages must be at least 1")

    scraper = PropertyScraper()
    records = scraper.scrape(
        args.url,
        max_pages=args.pages
    )

    save_results(
        records,
        ROOT / args.output
    )


if __name__ == "__main__":
    main()
