from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

#the search field
search_word = 'nitro tech'

splited_search_word = search_word.replace(" ", "+")

url = f"https://www.amazon.com/s?k={splited_search_word}&ref=nb_sb_noss_2"

# selenim settings
path = "C:\\Program Files (x86)\\chromedriver.exe"
options = Options()
options.headless = False
driver = webdriver.Chrome(path, options=options)

supplements = []

def scrape_product(url):
	driver.get(url)
	time.sleep(2)

	#beautifulsuop
	soup = BeautifulSoup(driver.page_source, 'lxml')
	products = soup.find_all("div", class_="a-section a-spacing-medium")
	for product in products:
		print(" ")
		try:
			title = product.find("span", class_="a-size-base-plus a-color-base a-text-normal").text
		except:
			title = "weight is not provided"

		try:
			price = product.find("span", class_="a-offscreen").text
		except:
			price = "weight is not provided"

		try:
			weight = product.find("span", class_="a-color-information a-text-bold").text
		except:
			weight = "weight is not provided"

		supplement = (title, price, weight)
		supplements.append(supplement)


	return soup

soup = scrape_product(url)

new_pages = True

while new_pages:
	try:
		next_page_url = soup.find("li", class_="a-last").a["href"]
		new_url = "https://www.amazon.com/" + next_page_url
		soup = scrape_product(new_url)
	except:
		new_pages = False

#saving the data to a csv file
df = pd.DataFrame(supplements, columns=['Title','price','weight'])
df.to_csv('nitro_tech_amazon.csv', index=False, encoding='utf-8')
