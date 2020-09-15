from bs4 import BeautifulSoup
import requests

carSelector = '.ListingItemTitle-module__container'

url = 'https://auto.ru/moskva/cars/{}/all/?page={}&output_type=list'

result = requests.get(url.format('lexus', 1))

soup = BeautifulSoup(result.content, 'html.parser')

resultList = []

for car in soup.select(carSelector):
    resultRow = []

    resultRow.append(car.select_one('.Link.ListingItemTitle-module__link').text)
    try:
        resultRow.append(car.select_one('.ListingItemPrice-module__content').text)
    except Exception:
        resultRow.append(None)

    resultList.append(resultRow)

print(resultList)