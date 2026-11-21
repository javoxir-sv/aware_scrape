import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth


# Loads all the api_data that is not related to query but related to context

async def fetch_api_data(url, query="TAS2511MOW1"):
    async with Stealth().use_async(async_playwright()) as p:
        # load the browser
        browser = await p.chromium.launch(
                # usus my daily driving browser, so it avoids bot detection more effectively
            executable_path="/usr/bin/brave-origin",
            headless=False,)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"),
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()

        # load the website
        print("Loading Aviasales website...")
        await page.goto("https://www.aviasales.com/", wait_until="networkidle", timeout=60000)

        api_data = {}
        async def handle_response(response):
            if url in response.url:
                if response.status == 200:
                    nonlocal api_data
                    api_data = await response.json()
                    print("Successfully captured API response.")
                    
        page.on("response", handle_response)

        print("Performing search navigation...")
        await page.goto(
            f"https://www.aviasales.com/search/{query}",
            wait_until="domcontentloaded")

        await asyncio.sleep(10)

        if api_data:
            print(f"Flight Results Data by Query: {query}:", api_data)
        else:
          print("API response wasn't captured.")

        await browser.close()


# this is temporary here
gql_api = "https://ariadne.aviasales.com/api/gql"
tickets_api = "https://tickets-api.aviasales.com/search/v2/start"

market_change_dialog = {"query":"\n  query GetMarketsAndCountries($locales: [String!]!) {\n    market_change_dialog_v1 {\n      markets {\n        code\n      }\n      countries {\n        iata\n        translations(filters: { locales: $locales })\n      }\n    }\n  }\n","variables":{"locales":["en"]},"operation_name":"market_and_countries"}

recommendations = {"query":"\n    query EmptyAutocompletePlacesV1(\n      $input: EmptyAutocompletePlacesV1Input!,\n      $brand: Brand!\n      $locales: [String!]\n    ) { \n      empty_autocomplete_places_v1(\n      input: $input,\n      brand: $brand\n      ) {\n      __typename\n      recommendations\n      {\n      __typename\n      rec_id\n      items \n        { \n        __typename\n         city_info \n        {\n          __typename\n         city \n          { \n          __typename\n          iata\n           translations(filters: {locales: $locales})\n           country \n            { \n            __typename\n            iata\n            translations(filters: {locales: $locales})\n            }\n          }\n        image_url\n        }\n      reason\n      }\n    }\n  }\n}","variables":{"brand":"AS","locales":["en"],"input":{"origin_iata":"TAS","origin_type":null,"market":"us","language":"en","auid":"fwAAAWr1u/SfiAAKAyE6Ag==","limit":6}},"operation_name":"empty_autocomplete_places_v1"}


url_list = {
         "auid": "https://www.aviasales.com/auid/refresh",
         "batch": "https://flagr.aviasales.com/api/v1/evaluation/batch?entityId=fwAAAWr1u%2FSfiAAKAyE6Ag%3D%3D&flagTag=salo-web&brand=%22AS%22&environment=%22production%22&lang=%22en%22&market=%22us%22&platform=%22web%22&auid=%22fwAAAWr1u%2FSfiAAKAyE6Ag%3D%3D%22&web_client=%22web_desktop%22",
         "nearest_places": "https://suggest.aviasales.com/v2/nearest_places.json?locale=en_US",
         "config_market_us": "https://seo-currency-config.aviasales.com/config?market=us",
         "currency": "https://tickets-api.aviasales.com/currency.json",
         "code_to_places": "https://suggest.aviasales.com/v2/code_to_places.json?locale=en_US&term=TAS",
         "start": "https://tickets-api.aviasales.com/search/v2/start",
         "ribbon": "https://tickets-api.aviasales.com/search/prices/ribbon?origin=TAS&origin_type=city&destination=MOW&destination_type=city&currency=USD&brand=AS&market=us&trip_class=Y&passengers_adults=1&passengers_children=0&passengers_infants=0&is_one_way=true&filters_state=%7B%7D&depart_date_min=2026-11-16&depart_date_max=2026-12-31",
         "results": "https://tickets-api.eu-north-1.aviasales.com/search/v3.2/results",
        }

if __name__ == "__main__":
    url="tickets-api.eu-north-1.aviasales.com/search/v3.2/results"
    asyncio.run(fetch_api_data(url))


