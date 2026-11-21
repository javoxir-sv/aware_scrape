import requests
import time



url = "https://eticket.uzrailpass.uz/api/v1/csrf-token"
headers = {
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
            ),
        "accept": "application/json",
        "device-type": "BROWSER",
        "referer": "https://eticket.uzrailpass.uz/uz/pages/trains-page",
        }

print("Getting the cookies...")
response = requests.get(url, headers=headers)

cookies = response.cookies.get_dict()
# filter out None values, so python don't complain it
cookies = {
    key: value
    for key, value in cookies.items()
    if value is not None
}

text = response.text
print(cookies)


with open("session/session.txt", "w") as file:
    file.write(f"cookies: {cookies}\n\ntext: {text}")

print("Got the CSRF token.")

print("Wait a bit...")
time.sleep(5)

# to get the data
payload = {"directions":{"forward":{"date":"2026-11-22","depStationCode":"2900700","arvStationCode":"2900000"}},"routeType":"INTERCITY"}
list_url = "https://eticket.uzrailpass.uz/api/v3/handbook/trains/list"
list_headers = {
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
            ),
        "accept": "application/json",
        "accept-language": "uz",
        "device-type": "BROWSER",
        "referer": "https://eticket.uzrailpass.uz/uz/pages/trains-page",
        "origin": "https://eticket.uzrailpass.uz",
        "cookie": f"XSRF-TOKEN={cookies['XSRF-TOKEN']}",
        "x-xsrf-token": cookies["XSRF-TOKEN"],
        }


print("Getting the list data...")
list_response = requests.post(url=list_url, headers=list_headers, json=payload)

print("Status:", list_response.status_code)
print("Response (text):", list_response.text)
print("Response (json):", list_response.json())

