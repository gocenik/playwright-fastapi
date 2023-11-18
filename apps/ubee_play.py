from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from playwright.async_api import async_playwright

app = FastAPI()

class LoginInfo(BaseModel):
    username: str
    password: str
    url: str

async def run_playwright(username: str, password: str, url: str):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)

            # Check if the specific fields are visible
            if await page.is_visible("input[name=\"c_UserId\"]"):
                # Fill in the first form if present
                await page.fill("input[name=\"c_UserId\"]", username)
                await page.fill("input[name=\"c_Password\"]", password)
                await page.fill("input[name=\"c_PasswordReEnter\"]", password)
                await page.click("text=Apply")
                # Wait for the page to reload
                await page.wait_for_load_state("networkidle")

            # Fill in the login form
            await page.fill("input[name=\"loginUsername\"]", username)
            await page.fill("input[name=\"loginPassword\"]", password)
            await page.click("text=Login")
            # Wait for the page to load after login
            await page.wait_for_load_state("networkidle")

            # Navigate to the system info page
            await page.goto(f"{url}/UbeeSysInfo.asp")
            # Fetch system info

            model = await page.text_content('table:nth-child(1) tr:nth-child(3) > td:nth-child(2)')
            hardware_version = await page.text_content('table:nth-child(1) tr:nth-child(4) > td:nth-child(2)')
            firmware_version = await page.text_content('tr:nth-child(5) > td:nth-child(2)')
            boot_version = await page.text_content('tr:nth-child(6) > td:nth-child(2)')
            serial_number = await page.text_content('tr:nth-child(7) > td:nth-child(2)')
            mac_address = await page.text_content('tr:nth-child(8) > td:nth-child(2)')
            network_access = await page.text_content('table:nth-child(4) tr:nth-child(3) > td:nth-child(2)')

            await browser.close()
            return {
                "model": model,
                "hardware_version": hardware_version,
                "firmware_version": firmware_version,
                "boot_version": boot_version,
                "serial_number": serial_number,
                "mac_address": mac_address,
                "network_access": network_access
            }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

@app.post("/run_system_info_reader/")
async def run_system_info_reader(login_info: LoginInfo):
    return await run_playwright(login_info.username, login_info.password, login_info.url)