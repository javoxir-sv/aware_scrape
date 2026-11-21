import argparse
import json
import time
import os
from get_csrf import get_csrf_token
from fetch_data import fetch_data

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Temir yo'llari automated query based scraper"
        )
    )

    # Dynamic route search parameters
    parser.add_argument(
        "--from",
        dest="origin",
        default="2900700",
        help="Origin city train station code (default: 2900700)",
    )
    parser.add_argument(
        "--to",
        dest="destination",
        default="2900000",
        help="Destination city train station code (default: 2900000)",
    )
    parser.add_argument(
        "-d",
        "--date",
        default="2026-11-22",
        help=(
            "Departure date in YYYY-MM-DD format, e.g. 2026-11-22 for Nov 22 (default: 2026-11-22)"
        ),
    )
    parser.add_argument(
        "-t",
        "--type",
        default="INTERCITY",
        help=(
            "Train route direction (default: INTERCITY)"
        )
    )
    parser.add_argument(
        "-w",
        "--wait",
        type=int,
        default=5,
        help=(
            "Seconds to wait between gettinf the CSRF token and making a POST request to the backend api (default: 5)"
        )
    )

    # Construct payload
    args = parser.parse_args()
    payload = {
            "directions":{
                "forward":{
                    "date": args.date,
                    "depStationCode":args.origin,
                    "arvStationCode":args.destination,
                    }
                },
            "routeType":args.type
            }

    # Getting the saved CSRF token
    print("[-] Loading the saved CSRF token if exists...")
    if os.path.isfile("session/csrf.json"):
        with open("session/csrf.json", "r") as f:
            csrf_json = json.load(f)
        csrf_token = csrf_json["XSRF-TOKEN"]
    else:
        print("[-] Saved CSRF token doesn't exist, issuing new CSRF token...")
        csrf_token = get_csrf_token()

    print(f"[-] Waiting {args.wait} seconds to not to trigger anything...")
    time.sleep(args.wait)

    # Establishing connections with the server and getting the data
    def get_data(csrf_token, i):
        if i <= 1:
            print("[-] Making a post request to the backend api...")
            response = fetch_data(csrf_token, payload)
            print("[-] Status code:", response.status_code)

            if response.status_code == 200:
                with open("data/search_results.json", "w") as f:
                    json.dump(response.json(), f, indent=4)
                print("[+] Saved: data/search_results.json")

            elif response.status_code in (400, 401, 403, 419):
                print("[!] Possible CSRF token expiration. Issuing new CSRF token...")
                csrf_token = get_csrf_token()
                print("[-] Re-tring to get the data...")
                get_data(csrf_token, i)
            else:
                print("[!] Failed to establish communication with the backend api, can't be helped.")
        else:
            print("[!] Failed to establish communication with the backend api, can't be helped.")
            exit()

    get_data(csrf_token, i=0)


if __name__ == "__main__":
    main()
