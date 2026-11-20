# Aviasales Scraper Configuration and Payloads

GQL_API = "https://ariadne.aviasales.com/api/gql"
TICKETS_API_START = "https://tickets-api.aviasales.com/search/v2/start"

URL_LIST = {
    "auid": "https://www.aviasales.com/auid/refresh",
    "batch": (
        "https://flagr.aviasales.com/api/v1/evaluation/batch?entityId=fwAAAWr1u"
        "%2FSfiAAKAyE6Ag%3D%3D&flagTag=salo-web&brand=%22AS%22&environment=%22"
        "production%22&lang=%22en%22&market=%22us%22&platform=%22web%22&auid=%22"
        "fwAAAWr1u%2FSfiAAKAyE6Ag%3D%3D%22&web_client=%22web_desktop%22"
    ),
    "nearest_places": (
        "https://suggest.aviasales.com/v2/nearest_places.json?locale=en_US"
    ),
    "config_market_us": (
        "https://seo-currency-config.aviasales.com/config?market=us"
    ),
    "currency": "https://tickets-api.aviasales.com/currency.json",
    "code_to_places": (
        "https://suggest.aviasales.com/v2/code_to_places.json?locale=en_US&term=TAS"
    ),
}

MARKET_CHANGE_DIALOG_PAYLOAD = {
    "query": """
      query GetMarketsAndCountries($locales: [String!]!) {
        market_change_dialog_v1 {
          markets {
            code
          }
          countries {
            iata
            translations(filters: { locales: $locales })
          }
        }
      }
    """,
    "variables": {"locales": ["en"]},
    "operation_name": "market_and_countries",
}

