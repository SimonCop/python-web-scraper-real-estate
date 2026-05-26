import csv
import re
import time
import requests
from bs4 import BeautifulSoup


def scrape_bezrealitky():
    # URL pro prodej bytů v Praze (můžeš změnit podle potřeby)
    url = "https://www.bezrealitky.cz/vyhledat?by-typy-nemovitosti=byt&by-typy-nabidky=prodej&region-uri=praha"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("Spouštím scraper, stahuji data...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Chyba při načítání stránky: Kód {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Nalezení všech karet s inzeráty
    listings = soup.find_all("article")

    scraped_data = []

    for item in listings:
        try:
            # 1. Nadpis / Dispozice (např. "Prodej bytu 2+kk")
            title_element = item.find("h2")
            title = (
                title_element.text.strip()
                if title_element
                else "Neznámá dispozice"
            )

            # 2. Lokalita
            location_element = item.find(
                "span", class_=re.compile("Header_boxAddress")
            )
            if not location_element:
                location_element = item.find("p", class_=re.compile("address"))
            location = (
                location_element.text.strip() if location_element else "Praha"
            )

            # 3. Cena
            price_element = item.find(
                "span", class_=re.compile("Price_boxPrice")
            )
            if not price_element:
                price_element = item.find("strong", class_=re.compile("price"))

            if price_element:
                # Očištění ceny od znaků jako Kč, mezery atd.
                price_text = price_element.text.strip()
                price = re.sub(r"[^\d]", "", price_text)
            else:
                price = "Dohodou"

            scraped_data.append(
                {"Dispozice": title, "Lokalita": location, "Cena (Kč)": price}
            )

        except Exception as e:
            # Pokud jeden inzerát selže, pokračujeme dál
            print(f"Chyba při parsování inzerátu: {e}")
            continue

    # Uložení dat do CSV
    if scraped_data:
        save_to_csv(scraped_data)
    else:
        print("Nenalezena žádná data ke stažení.")


def save_to_csv(data):
    filename = "reality_vystup.csv"
    keys = data[0].keys()

    with open(
        filename, "w", newline="", encoding="utf-8-sig"
    ) as output_file:  # utf-8-sig zajistí správné zobrazení češtiny v Excelu
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    print(f"Hotovo! Data byla úspěšně uložena do souboru: {filename}")


if __name__ == "__main__":
    scrape_bezrealitky()
