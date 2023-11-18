from fastapi import APIRouter
from pydantic import BaseModel
from playwright.async_api import async_playwright

router = APIRouter()



class LoginInfo(BaseModel):
    username: str
    password: str
    url: str

async def run_playwright(username: str, password: str, url: str):
    try:
        async with async_playwright() as p:
            browser = await p.webkit.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)

            # Check if device was reseted
            await page.goto(url)
            if await page.locator("input[name=\"c_UserId\"]").is_visible():
                print("Filling the first form")
                await page.locator("input[name=\"c_UserId\"]").fill(username)
                await page.locator("input[name=\"c_Password\"]").fill(password)
                await page.locator("input[name=\"c_PasswordReEnter\"]").fill(password)
                await page.locator("button:has-text(\"Apply\")").click()  
                
            print("Filling the main login form")
            await page.locator("input[name=\"loginUsername\"]").fill(username)
            await page.locator("input[name=\"loginPassword\"]").fill(password)
            await page.locator("input[name=\"loginPassword\"]").press("Enter")  # Or click on the login button if there is one

            # Navigate to the system info page
            await page.goto(f"{url}/UbeeSysInfo.asp")
            # Fetch system info

            # model = await page.text_content('table:nth-child(1) tr:nth-child(3) > td:nth-child(2)')
            hardware_version = await page.text_content('table:nth-child(1) tr:nth-child(4) > td:nth-child(2)')
            firmware_version = await page.text_content('tr:nth-child(5) > td:nth-child(2)')
            boot_version = await page.text_content('tr:nth-child(6) > td:nth-child(2)')
            serial_number = await page.text_content('tr:nth-child(7) > td:nth-child(2)')
            mac_address = await page.text_content('tr:nth-child(8) > td:nth-child(2)')
            network_access = await page.text_content('table:nth-child(4) tr:nth-child(3) > td:nth-child(2)')

            await browser.close()
            return {
                # "model": model,
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

@router.post("/run_system_info_reader/")
async def run_system_info_reader(login_info: LoginInfo):
    return await run_playwright(login_info.username, login_info.password, login_info.url)