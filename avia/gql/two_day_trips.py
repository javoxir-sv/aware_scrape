import requests
import json
from config import get_config

# load config
config = get_config()
headers = config.get("headers")

URL = "https://explore-api.aviasales.com/v1/weekend_prices/list.json?currency=usd&direct=false&language=en&market=us&origin=TAS&origin_type=CITY&period_holidays=false&period_weekends=false&sort_type=popularity&with_baggage=false"

response = requests.get(
    URL,
    headers=headers,
    timeout=30
)

print("Status:", response.status_code)

response.raise_for_status()

result = response.json()

with open("data/two_day_trips.json", "w") as file:
    json.dump(result, file, indent=2, ensure_ascii=False)

print("Finished. Saved to: data/two_day_trips.json")

