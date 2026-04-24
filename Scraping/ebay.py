from selenium.webdriver.common.keys import Keys

from scraper import Scraper
from scraper import Selectors
import time

def filter(items, string):
    total, matches = 0, 0
    for item in items:
        if item in string: matches += 1
        total += 1
    
    if matches/total >= 0.7: return True
    return False

dic = {}
item = input("Enter item: ").lower()
items = item.split()

webscraper = Scraper(10, True)
webscraper.get("https://www.ebay.com/")
time.sleep(1)

searchbox = webscraper.find(Selectors.CSS_SELECTOR, ".gh-search-input.gh-tb.ui-autocomplete-input")
searchbox.send_keys(item + Keys.ENTER)
time.sleep(1)

cards = webscraper.find_all(Selectors.CSS_SELECTOR, ".s-item__wrapper.clearfix")
time.sleep(1)

print("\n\n\n")
for card in cards[:15]:
    product = webscraper.find_in(card, Selectors.CLASS_NAME, "s-item__title")
    if product and filter(item, product.text.lower()):
        price = webscraper.find_in(card, Selectors.CLASS_NAME, "s-item__price")
        dic[product.text] = price.text
print("\n\n\n")

for key, value in dic.items():
    print(f"{key}: {value}")

webscraper.quit()