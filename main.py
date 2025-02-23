from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Povoliť požiadavky zo všetkých domén
    allow_credentials=True,
    allow_methods=["*"],  # Povoliť všetky HTTP metódy (GET, POST, ...)
    allow_headers=["*"],  # Povoliť všetky HTTP hlavičky
)

@app.get("/")
def home():
    return {"message": "FastAPI beží správne!"}

@app.get("/scrape-hn")
def scrape_hn():
    url = "https://news.ycombinator.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Nájdeme všetky nadpisy článkov
        articles = []
        for item in soup.find_all("span", class_="titleline"):
            title_tag = item.find("a")
            if title_tag:
                title = title_tag.text
                link = title_tag["href"]
                articles.append({"title": title, "link": link})
        
        return {"articles": articles}
    
    return {"error": "Page not accessible"}
