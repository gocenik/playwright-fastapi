from playwright.async_api import async_playwright
from urllib.parse import urlparse
import logging

class RestartError(Exception):
    pass

async def restart(url: str, selector1: str = '[name="RebootYes"]', selector2: str = '#ID_LABEL_TABLE_CONF_REBOOT_APPLY'):
    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL")

        async with async_playwright() as p:
            browser = await p.webkit.launch(headless=True)
            page = await browser.new_page()
            await page.goto(f"{url}/UbeeConfiguration.asp")

            # Click on the button to initiate reboot
            await page.click(selector1)

            # Confirm the reboot
            await page.click(selector2)

            # Add any necessary wait or verification step here if needed

            await browser.close()

        return "Restart successful"

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise RestartError(str(e))
    
    
