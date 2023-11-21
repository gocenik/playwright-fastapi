import asyncio
from playwright.async_api import async_playwright

class UbeeTelephonyInfoReader:

    async def run_telephony_info_reader(self, ubee_url):
        print("Running Telephony Info Reader")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"{ubee_url}/UbeeTelStatus.asp")

                # Reading telephony information
                dhcp_status = await page.text_content("table:nth-child(2) tr:nth-child(2) > td:nth-child(2)")
                print(f"DHCP Status read: {dhcp_status}")
                telephony_provisioning = await page.text_content("#ID_LABEL_MTAPROV_INPROGRESS")
                print(f"Telephony Provisioning read: {telephony_provisioning}")
                registered_with_call_server = await page.text_content("tr:nth-child(6) > td:nth-child(2)")
                print(f"Registered with Call Server status read: {registered_with_call_server}")
                port1_status = await page.text_content("table:nth-child(3) tr:nth-child(2) > td:nth-child(2)")
                print(f"Port 1 Status read: {port1_status}")
                port2_status = await page.text_content("table:nth-child(3) tr:nth-child(3) > td:nth-child(2)")
                print(f"Port 2 Status read: {port2_status}")

                await browser.close()

                return {
                    "dhcp_status": dhcp_status,
                    "telephony_provisioning": telephony_provisioning,
                    "registered_with_call_server": registered_with_call_server,
                    "port1_status": port1_status,
                    "port2_status": port2_status
                }
        finally:
            await browser.close()

    except LoginError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred."}