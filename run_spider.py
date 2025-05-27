from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd



service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)



data = []


url = "https://www.divan.ru/category/svet"
driver.get(url)
time.sleep(3)

while True:
    products = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")
    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, "a[class*='ProductName'] span").text.strip()
            link = product.find_element(By.CSS_SELECTOR, "a[class*='ProductName']").get_attribute("href")
            price = product.find_element(By.CSS_SELECTOR, "span[data-testid='price']").text.strip() + " ₽"
        except Exception:
            continue

        data.append({
            "Название": name,
            "Ссылка": link,
            "Цена": price
        })


    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a.Pagination__Next")
        next_link = next_btn.get_attribute("href")
        if not next_link:
            break
        driver.get(next_link)
        time.sleep(2)
    except Exception:
        break


driver.quit()


df = pd.DataFrame(data)
df.to_csv("divan_lights.csv", index=False, encoding="utf-8-sig")

print("Данные сохранены в divan_lights.csv")
