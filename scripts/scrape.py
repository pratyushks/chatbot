import os
import asyncio
from playwright.async_api import async_playwright

OUTPUT_DIR = "./data/Angelone_scrapped"
BASE_URL = "https://www.angelone.in/support"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL, timeout=60000)

        await page.wait_for_selector("text=Learn More")

        links = await page.eval_on_selector_all(
            "a:has-text('Learn More')",
            "elements => elements.map(el => el.href)"
        )

        print(f"Found {len(links)} category pages.")

        for link in links:
            await page.goto(link, timeout=60000)
            await page.wait_for_load_state("domcontentloaded")
            text = await page.evaluate("() => document.body.innerText")

            filename = os.path.join(OUTPUT_DIR, link.replace("/", "_").replace(":", "") + ".txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text.strip())

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape())
