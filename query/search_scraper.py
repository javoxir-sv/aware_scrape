import asyncio
import json
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# for round trip TAS 1012 TYO 1301 MOW 1

async def scrape_search_results(
    headless=True, use_brave=False, route_query="TAS2511MOW1", profile_dir="session/browser_profile"
):
    print(f"[-] Starting dynamic search scraper for route: {route_query}...")

    captured_data = {
        "ribbon": False,
        "results": False,
        "start": False,
    }

    # async with async_playwright() as p:
    async with Stealth().use_async(async_playwright()) as p:
        if use_brave:
            browser = await p.chromium.launch(
                # usus my daily driving browser, so it avoids bot detection more effectively
                executable_path="/usr/bin/brave-origin",
                headless=headless,
            )
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"),
                viewport={
                    "width": 1365,
                    "height": 768,
                },
                screen={
                    "width": 1365,
                    "height": 768,
                },
                storage_state="session/session_state.json"
            )

        else:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                executable_path="/usr/bin/chromium",
                headless=headless,
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like"
                    " Gecko) Chrome/156.0.0.0 Safari/537.36"
                ),
                viewport={
                    "width": 1365,
                    "height": 768,
                },
                screen={
                    "width": 1365,
                    "height": 768,
                },
            )

        page = context.pages[0] if context.pages else await context.new_page()

        async def handle_response(response):
            url = response.url
            if response.status == 200:
                if "tickets-api.aviasales.com/search/prices/ribbon" in url:
                    try:
                        captured_data["ribbon"] = await response.json()
                        print("[+] Captured Ribbon API response!")
                    except Exception as e:
                        print(f"[!] Error parsing ribbon json: {e}")
                elif (
                    "tickets-api.eu-north-1.aviasales.com/search/v3.2/results"
                    in url
                ):
                    try:
                        captured_data["results"] = await response.json()
                        print("[+] Captured Flight Results API response!")
                    except Exception as e:
                        print(f"[!] Error parsing results json: {e}")
                elif (
                    "https://tickets-api.aviasales.com/search/v2/start" in url
                ):
                    try:
                        captured_data["start"] = await response.json()
                        print("[+] Captured Start API response!")
                    except Exception as e:
                        print(f"[!] Error parsing start json: {e}")

        page.on("response", handle_response)

        print("[-] Navigating to homapage first: https://www.aviasales.com/")
        await page.goto("https://www.aviasales.com/", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(5)

        search_url = f"https://www.aviasales.com/search/{route_query}"
        print(f"[-] Navigating to search URL: {search_url}")
        await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)

        print("[-] Waiting for background API requests to finish...")
        await asyncio.sleep(12)

        os.makedirs("data", exist_ok=True)

        if captured_data["ribbon"]:
            with open("data/search_ribbon.json", "w") as f:
                json.dump(captured_data["ribbon"], f, indent=2)
            print("[+] Saved data/search_ribbon.json")

        if captured_data["results"]:
            with open("data/search_results.json", "w") as f:
                json.dump(captured_data["results"], f, indent=2)
            print("[+] Saved data/search_results.json")

        if captured_data["start"]:
            with open("data/search_start.json", "w") as f:
                json.dump(captured_data["start"], f, indent=2)
            print("[+] Saved data/search_start.json")

        else:
            print(
                "[!] Flight results response was not automatically"
                " intercepted. Check search route."
            )

        await context.close()
        if use_brave:
            try:
                await browser.close()
            finally:
                print("[-] Couldn't close the browser instance, please close it yourself.")

if __name__ == "__main__":
    asyncio.run(scrape_search_results())
