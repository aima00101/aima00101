import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/page-{}.html"
products = []

for page in range(1, 51):  # الموقع فيه 50 صفحة
    response = requests.get(base_url.format(page))
    response.encoding = "utf-8"  # تصحيح ترميز الصفحة
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".product_pod")

    for item in items:
        title = item.h3.a["title"]

        # تنظيف السعر من أي رموز غريبة
        price_text = item.select_one(".price_color").get_text()
        price_text = price_text.replace("£", "").replace("Â", "").strip()
        try:
            price = float(price_text)
        except:
            price = None

        # تحويل التقييم من كلمة لرقم
        rating_text = item.p["class"][1]  # "One", "Two", ...
        rating_map = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
        rating = rating_map.get(rating_text, None)

        availability = item.select_one(".availability").get_text(strip=True)

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "in_stock": "In stock" in availability
        })

df = pd.DataFrame(products)

# إزالة أي بيانات ناقصة
df.dropna(inplace=True)

# حفظ CSV
df.to_csv("books_full.csv", index=False)
print("✅ Scraping complete! CSV saved as books_full.csv")
df.head()
