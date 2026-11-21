import requests
import json

def get_csrf_token():
    url = "https://eticket.uzrailpass.uz/api/v1/csrf-token"
    headers = {
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
                ),
            "accept": "application/json",
            "accept-language": "uz",
            "device-type": "BROWSER",
            "referer": "https://eticket.uzrailpass.uz/uz/pages/trains-page",
            }

    response = requests.get(url, headers=headers)
    cookies = response.cookies.get_dict()
    # filter out None values, so python don't complain it
    cookies = {
        key: value
        for key, value in cookies.items()
        if value is not None
    }

    print(f"[+] Recieved new CSRF token: {cookies}")
    with open("session/csrf.json", "w") as f:
        json.dump(cookies, f, indent=4)

    return cookies['XSRF-TOKEN']
