import asyncio
from playwright.async_api import async_playwright


async def fetch_flight_results():
  async with async_playwright() as p:
    # Launch browser (set headless=False if you want to watch it work and solve any initial CAPTCHAs manually)
    browser = await p.chromium.launch(
            executable_path="/usr/bin/chromium",
            headless=False,  # Set to True if you don't need a visible window
        )
    context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like"
                " Gecko) Chrome/156.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )

    page = await context.new_page()

    # 1. Navigate to Aviasales to establish cookies, session, and pass AWS WAF checks
    print("Navigating to Aviasales to clear security checks...")
    await page.goto(
        "https://www.aviasales.com/", wait_until="networkidle", timeout=60000
    )

    # 2. Intercept the specific API call when the frontend triggers a search results fetch,
    # OR navigate directly to a search URL if you have a pre-generated search link.
    # Alternatively, you can listen to responses:
    api_data = {}
    async def handle_response(response):
        print("Response URL:", response.url)
        if "tickets-api.eu-north-1.aviasales.com/search/v3.2/results" in response.url:
            if response.status == 200:
              nonlocal api_data
              api_data = await response.json()
              print("Successfully captured API response!")

    page.on("response", handle_response)

    # 3. Trigger a search or visit a direct search results URL on Aviasales
    # (Example: searching flights from Tashkent to Moscow)
    print("Performing search navigation...")
    await page.goto(
        "https://www.aviasales.com/search/TAS2511MOW1",
        wait_until="domcontentloaded",
    )

    # Wait a bit for the XHR/fetch requests to complete and trigger our event listener
    await asyncio.sleep(10)

    if api_data:
      print("Flight Results Data:", api_data)
    else:
      print(
          "API response wasn't automatically captured. You may need to adjust"
          " the search route URL."
      )

    await browser.close()


asyncio.run(fetch_flight_results())
