from fastapi import APIRouter
from pydantic import BaseModel
from pyppeteer import launch

from base64 import b64encode


router = APIRouter()

class WebshotModel(BaseModel):
    url: str

class Launcher:
    async def __aenter__(self):
        self.browser = await launch()
        return self.browser
    
    async def __aexit__(self, *args):
        await self.browser.close()

@router.post("/webshot", response_model=WebshotModel)
async def webshot(webshot):
    async with Launcher() as browser:
        page = await browser.newPage()
        try:
            await page.goto(webshot.url)
        except Exception as e:
            return {"status": False, "message": e}
        else:
            image_byte = await page.screenshot()
            return {"status": True, "image": b64encode(image_byte)}
