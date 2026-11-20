# Aviasales Scraper Configuration and Payloads

GQL_API = "https://ariadne.aviasales.com/api/gql"
TICKETS_API_START = "https://tickets-api.aviasales.com/search/v2/start"

URL_LIST = {
    "auid": "https://www.aviasales.com/auid/refresh",
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

