import requests
import json
from config import get_config

# load config
config = get_config()

# load payload
with open("payload/popular_destinations.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

# load headers from config
URL = config.get("gql_endpoint")
headers = config.get("headers")

response = requests.post(
    URL,
    headers=headers,
    json=payload,
    timeout=30
)

print("Status:", response.status_code)

response.raise_for_status()

result = response.json()

if result.get("errors"):
    print("\nGraphQL errors:")
    print(json.dumps(result["errors"], indent=2))
    raise SystemExit(1)

# save the json response
with open("data/popular_destinations.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

blocks = result["data"]["main_page_blocks_v1"]["blocks"]

print(f"\nTotal blocks: {len(blocks)}")

for i, block in enumerate(blocks):
    print(f"{i + 1}. {block.get('__typename')}")

print("\nPOPULAR DESTINATIONS:")

for block in blocks:

    if block.get("__typename") != "PopularDestinationsBlock":
        continue

    origin = block.get("origin_city", {})

    print("\nOrigin:", origin.get("iata"))

    for destination in block.get("directions", []):

        price = destination.get("min_price") or {}

        print({
            "country": destination.get("country_iata"),
            "image_url": destination.get("image_url"),
            "price": price.get("value"),
            "currency": price.get("currency")
        })

print("\nFull JSON saved to response.json")
