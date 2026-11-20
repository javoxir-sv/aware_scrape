import argparse
import asyncio
from browser_session import capture_session_state
from search_scraper import scrape_search_results
from static_scraper import scrape_static_endpoints


async def main():
    parser = argparse.ArgumentParser(
        description=(
            "Aviasales Automated Scraper & Search CLI with Conditional Static"
            " Loading"
        )
    )

    # Initialization flag
    parser.add_argument(
        "-i",
        "--initialize",
        action="store_true",
        help=(
            "Download query-independent static data and capture fresh browser"
            " session WAF tokens. (If omitted, uses cached data/sessions)."
        ),
    )


    parser.add_argument(
        "-d",
        "--headed",
        action="store_true",
        help="Browser mode, emulate real browser (headed)",
    )

    parser.add_argument(
        "-b",
        "--brave",
        action="store_true",
        help="Use Brave Origin (default: False)",
    )

    # Dynamic route search parameters
    parser.add_argument(
        "--from",
        dest="origin",
        default="TAS",
        help="Origin city IATA code (default: TAS)",
    )
    parser.add_argument(
        "--to",
        dest="destination",
        default="MOW",
        help="Destination city IATA code (default: MOW)",
    )
    parser.add_argument(
        "--de-date",
        dest="de_date",
        default="",
        help=(
            "Departure date in DDMM format, e.g. 3011 for Nov 30 (30:day, 11:month)"
        ),
    )
    parser.add_argument(
        "--cb-date",
        dest="cb_date",
        default="",
        help=(
            "Comeback date in DDMM format, e.g. 2512 for Dec 25 (25:day, 12:month)"
        ),
    )
    parser.add_argument(
        "-p",
        "--passengers",
        type=int,
        default=1,
        help="Number of adult passengers (default: 1)",
    )

    args = parser.parse_args()

    print("=== Aviasales Scraper Orchestration ===")

    # Conditionally run query-independent static downloads only if -i is provided
    if args.initialize:
        print(
            "[-] Initialization flag (-i) detected. Downloading"
            " query-independent static data & refreshing session..."
        )
        scrape_static_endpoints()
        await capture_session_state(
            headless=not args.headed,
            use_brave=args.brave,
        )
    else:
        print(
            "[-] Skipping query-independent static data download (relying on"
            " cached files)."
        )

    # Construct dynamic route string (e.g. TAS3011MOW25121)
    route_query = (
        f"{args.origin.upper()}{args.de_date}{args.destination.upper()}{args.cb_date}{args.passengers}"
    )

    # Execute dynamic search scraper
    await scrape_search_results(
            headless=not args.headed,
            use_brave=args.brave,
            route_query=route_query
    )

    print("=== Scraper execution completed successfully! ===")


if __name__ == "__main__":
    asyncio.run(main())
