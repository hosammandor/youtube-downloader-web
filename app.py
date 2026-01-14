from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from yt_dlp import YoutubeDL

app = FastAPI()

# ملفات الواجهة
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_direct_link(url, format_type):
    url = url.strip()
    if not url:
        return None

    if format_type == "mp3":
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'skip_download': True}
    else:
        ydl_opts = {'format': 'best[ext=mp4]/best', 'quiet': True, 'no_warnings': True, 'skip_download': True}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if format_type == "mp4":
            if 'url' in info: return info['url']
            elif 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('ext') == 'mp4' and f.get('url'):
                        return f['url']
        else:
            if 'url' in info: return info['url']
            elif 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('acodec') != 'none' and f.get('url'):
                        return f['url']
    return None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "link": ""})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, url: str = Form(...), format_type: str = Form(...)):
    link = None
    try:
        link = get_direct_link(url, format_type)
    except Exception as e:
        link = f"Error: {str(e)}"
    return templates.TemplateResponse("index.html", {"request": request, "link": link})
