import json
import os
import requests
from config import (
    GQL_API,
    MARKET_CHANGE_DIALOG_PAYLOAD,
    URL_LIST,
)


def scrape_static_endpoints():
    print("[-] Scraping query-independent static & lookup endpoints...")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like"
            " Gecko) Chrome/156.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Origin": "https://www.aviasales.com",
        "Referer": "https://www.aviasales.com/",
    }

    os.makedirs("data", exist_ok=True)

    for name, url in URL_LIST.items():
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                file_path = os.path.join("data", f"static_{name}.json")
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"[+] Saved static data: {name} -> {file_path}")
            else:
                print(f"[!] Failed to fetch {name}: Status {resp.status_code}")
        except Exception as e:
            print(f"[!] Error fetching {name}: {e}")

    gql_queries = {
        "market_change_dialog": MARKET_CHANGE_DIALOG_PAYLOAD,
    }

    for name, payload in gql_queries.items():
        try:
            resp = requests.post(
                GQL_API,
                headers={**headers, "Content-Type": "application/json"},
                json=payload,
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                file_path = os.path.join("data", f"gql_{name}.json")
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"[+] Saved GraphQL static data: {name} -> {file_path}")
            else:
                print(f"[!] Failed GQL {name}: Status {resp.status_code}")
        except Exception as e:
            print(f"[!] Error fetching GQL {name}: {e}")


if __name__ == "__main__":
    scrape_static_endpoints()
