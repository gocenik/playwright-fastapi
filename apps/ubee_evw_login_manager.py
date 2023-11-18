# ubee_evw_login_manager.py
from playwright.async_api import async_playwright
import logging

from ubee_evw_system_info_reader import LoginException

async def perform_ubee_evw_login(username: str, password: str, url: str):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(url)
            
            if await page.locator("input[name=\"c_UserId\"]").is_visible():
                logging.info("Filling the reset form")
                await page.locator("input[name=\"c_UserId\"]").fill(username)
                await page.locator("input[name=\"c_Password\"]").fill(password)
                await page.locator("input[name=\"c_PasswordReEnter\"]").fill(password)
                await page.locator("button:has-text(\"Apply\")").click()  
                
            if await page.locator("input[name=\"loginUsername\"]").is_visible():
                logging.info("Filling the main login form")
                await page.locator("input[name=\"loginUsername\"]").fill(username)
                await page.locator("input[name=\"loginPassword\"]").fill(password)
                await page.locator("input[name=\"loginPassword\"]").press("Enter") 

            return browser, page
        
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        await browser.close()
        raise LoginException("An error occurred during login")