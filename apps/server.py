from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright

app = FastAPI()

class LoginInfo(BaseModel):
    username: str
    password: str
    url: str

@app.post("/login/")
async def login(login_info: LoginInfo):
    try:
        await run_playwright(login_info.username, login_info.password, login_info.url)
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def run_playwright(username: str, password: str, url: str):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)

            # Logic for handling different login forms
            # Add the necessary logic as per the structure of the login page you are targeting
            # ...

            # Ensure to close the browser after the operations are completed
            await browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
