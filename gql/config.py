import json

# for headers / reusability
def get_config():
    
    # get auid
    with open("payload/popular_destinations.json", "r", encoding="utf-8") as f:
        payload = json.load(f)
    auid = payload["variables"]["input"]["auid"]

    config = {
            "gql_endpoint": "https://ariadne.aviasales.com/api/gql",
            "headers": {
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.7",
                "content-type": "application/json",
                "origin": "https://www.aviasales.com",
                "referer": "https://www.aviasales.com/",
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                "client-device-info": f"type=desktop_web; auid={auid}",
                "x-auid": auid,
                "x-user-platform": "web",
                },

            }

    return config
