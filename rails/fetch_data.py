import requests

def fetch_data(csrf_token, payload):
    url = "https://eticket.uzrailpass.uz/api/v3/handbook/trains/list"
    headers = {
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
                ),
            "accept": "application/json",
            "accept-language": "uz",
            "content-type": "application/json",
            "device-type": "BROWSER",
            "referer": "https://eticket.uzrailpass.uz/uz/pages/trains-page",
            "origin": "https://eticket.uzrailpass.uz",
            "cookie": f"XSRF-TOKEN={csrf_token}",
            "x-xsrf-token": csrf_token,
            }

    response = requests.post(url=url, headers=headers, json=payload)
    return response

