import requests
from bs4 import BeautifulSoup
import smtplib
from config import MY_EMAIL, MY_PASSWORD, TO_EMAIL
import lxml

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
URL = "https://www.newegg.com/soundcore-sleep-a20-earbud-beige/p/0TH-033Y-000P4?Item=9SIACCUKAV8882&cm_sp=homepage_carousel_p6_electronics-_-item-_-9SIACCUKAV8882"

response = requests.get(url=URL, headers=headers)
product_html = response.text

soup = BeautifulSoup(product_html, "lxml")
el = soup.select_one("li.price-current strong")

if el:
    raw = el.getText().strip()           # e.g. "$1,299.99"
    price = float(raw.replace("$", "").replace(",", ""))
else:
    price = None

el = soup.find(name="h1", class_="product-title")
title = el.getText().strip() if el else None

if price < 120:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject:NewEgg Price Alert!\n\n{product_name} is now ${price}\n{URL}.".encode("utf8")
        )
