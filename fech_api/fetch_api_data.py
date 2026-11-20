import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

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



if __name__ == "__main__":
    url="tickets-api.eu-north-1.aviasales.com/search/v3.2/results"
    asyncio.run(fetch_api_data(url))


