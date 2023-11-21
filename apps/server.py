import logging
from xmlrpc.server import SimpleXMLRPCServer
import asyncio
from concurrent.futures import ThreadPoolExecutor
import playwright
import playwright.async_api as async_playwright
from enum import Enum

class ActionType(Enum):
    FETCH_TEXT = 1
    CLICK_BUTTON = 2
    INPUT_TEXT = 3

    def __init__(self, host, port):
        self.server = SimpleXMLRPCServer(("0.0.0.0", port))
        self.server.register_function(self.handle_web_action)
        self.server.register_function(self.login_to_ubee_sync)
        self.executor = ThreadPoolExecutor(max_workers=4)
        # ...

    def login_to_ubee_sync(self, username, password, url):
        # Synchronous wrapper for the async login_to_ubee method
        return asyncio.run(self.login_to_ubee(username, password, url))


    async def login_to_ubee(self, username, password, url):
        browser = await self.get_browser()
        page = await browser.new_page()
        await page.goto(url)

        # Check if device was reseted
        try:
            await page.locator("input[name=\"c_UserId\"]").fill(username)
            await page.locator("input[name=\"c_Password\"]").fill(password)
            await page.locator("input[name=\"c_PasswordReEnter\"]").fill(password)
            await page.locator("button:has-text(\"Apply\")").click()  
        except playwright.ElementHandleError:
            logging.info("Form is not visible")
            raise Exception("Form is not visible")
        except Exception as e:
            logging.error(f"Error in login_to_ubee: {e}")
            raise Exception("Error in login_to_ubee")

        logging.info("Filling the main login form")
        await page.locator("input[name=\"loginUsername\"]").fill(username)
        await page.locator("input[name=\"loginPassword\"]").fill(password)
        await page.locator("input[name=\"loginPassword\"]").press("Enter") 

        def login_to_ubee_sync(self, username, password, url):
            # Synchronous wrapper for the async login_to_ubee method
            return asyncio.run(self.login_to_ubee(username, password, url))

        return page

    def handle_web_action(self, url, action, params):
        # Wrapper function to run async task in the executor
        action_type = ActionType[action]
        future = asyncio.run_coroutine_threadsafe(
            self.perform_web_action(url, action_type, params), 
            asyncio.get_event_loop()
        )
        return future.result()

    def run_server(self):
        # Function to start the XMLRPC server
        self.server.serve_forever()

    async def perform_web_action(self, url, action: ActionType, params):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=5000)

                if action == ActionType.FETCH_TEXT:
                    selector = params.get('selector')
                    result = await self.fetch_text(page, selector)
                elif action == ActionType.CLICK_BUTTON:
                    selector = params.get('selector')
                    result = await self.click_button(page, selector)
                elif action == ActionType.INPUT_TEXT:
                    selector = params.get('selector')
                    text = params.get('text')
                    result = await self.input_text(page, selector, text)
                # Add more actions as needed
                # ...

                await page.close()
                return {'action': action.value, 'result': result}



        except playwright.ElementHandleError:
            logging.info("Form is not visible")
        except Exception as e:
            logging.error(f"Error in perform_web_action: {e}")
            return {'error': str(e)}

    async def run(self):
        await self.perform_web_action()


    async def fetch_text(self, page, selector):
        text = await page.text_content(selector)
        return {'text': text}

    async def click_button(self, page, selector):
        await page.click(selector, timeout=3000)
        return {'status': 'clicked'}

    async def input_text(self, page, selector, text):
        await page.fill(selector, text, timeout=3000)
        return {'status': 'text input'}


# Run the server
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = DeviceInfoServer('localhost', 5555)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, server.run_server)
    loop.run_forever()

