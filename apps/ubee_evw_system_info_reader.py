# ubee_evw_system_info_reader.py
from fastapi import APIRouter
from models import UbeeEVWLoginInfo
from models import UbeeEVWLoginInfo
from exceptions import LoginException

router = APIRouter()

@router.post("/run_system_info_reader/")
async def run_ubee_evw_system_info_reader(login_info: UbeeEVWLoginInfo):
    from ubee_evw_login_manager import perform_ubee_evw_login
    browser, page = await perform_ubee_evw_login(login_info.username, login_info.password, login_info.url)
    if not browser or not page:
        return {"error": "Login failed"}

    try:
        await page.goto(f"{login_info.url}/UbeeSysInfo.asp")
        # Fetch system info
        # model = await page.text_content('table:nth-child(1) tr:nth-child(3) > td:nth-child(2)')
        hardware_version = await page.text_content('table:nth-child(1) tr:nth-child(4) > td:nth-child(2)')
        firmware_version = await page.text_content('tr:nth-child(5) > td:nth-child(2)')
        boot_version = await page.text_content('tr:nth-child(6) > td:nth-child(2)')
        serial_number = await page.text_content('tr:nth-child(7) > td:nth-child(2)')
        mac_address = await page.text_content('tr:nth-child(8) > td:nth-child(2)')
        network_access = await page.text_content('table:nth-child(4) tr:nth-child(3) > td:nth-child(2)')
        if not hardware_version:
            raise HTTPException(status_code=500, detail="Hardware version not found")
        if not firmware_version:
            raise HTTPException(status_code=500, detail="Firmware version not found")
        if not boot_version:
            raise HTTPException(status_code=500, detail="Boot version not found")
        if not serial_number:
            raise HTTPException(status_code=500, detail="Serial number not found")
        if not mac_address:
            raise HTTPException(status_code=500, detail="MAC address not found")
        if not network_access:
            raise HTTPException(status_code=500, detail="Network access not found")
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
        logging.error(f"An error occurred: {e}")
        return {"error": str(e)}
    finally:
        await browser.close()
