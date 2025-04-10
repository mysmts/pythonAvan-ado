import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Salva no CSV
async def save_to_csv(data):
    async with asyncio.Lock():
        with open("books.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

# Extrai os dados dos livros da página
async def fetch_page(session, page):
    url = BASE_URL.format(page)
    async with session.get(url, headers=HEADERS) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        books = soup.select("article.product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text
            rating = book.p["class"][1]  # Ex: 'Three', 'Five', etc.
            print(title, price, rating)
            await save_to_csv([title, price, rating])

# Controla a execução assíncrona
async def main():
    with open("books.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Preço", "Avaliação"])

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page) for page in range(1, 6)]  # páginas 1 a 5
        await asyncio.gather(*tasks)

# Roda o script
if __name__ == "__main__":
    asyncio.run(main())
