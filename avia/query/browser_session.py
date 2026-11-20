import asyncio
import json
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth


async def capture_session_state(
    headless=True,
    use_brave=False,
    profile_dir="session/browser_profile",
    output_session_file="session/session_state.json",
):
    print(
        "[-] Launching Playwright to initialize session, cookies, and WAF"
        " tokens..."
    )
    os.makedirs(os.path.dirname(output_session_file), exist_ok=True)

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
                storage_state="session/session_state.json",
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

        print(
            "[-] Navigating to Aviasales to establish secure session & AWS WAF"
            " tokens..."
        )
        await page.goto(
            "https://www.aviasales.com/", wait_until="networkidle", timeout=70000
        )

        await asyncio.sleep(7)

        storage_state = await context.storage_state()
        with open(output_session_file, "w") as f:
            json.dump(storage_state, f, indent=2)
        print(f"[+] Session state and WAF tokens saved to {output_session_file}")

        await context.close()
        if use_brave:
            try:
                await browser.close()
            finally:
                print("[-] Couldn't close the browser instance, please close it yourself.")
        return output_session_file


if __name__ == "__main__":
    asyncio.run(capture_session_state())
