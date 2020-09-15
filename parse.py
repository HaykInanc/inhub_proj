from bs4 import BeautifulSoup
import requests
import csv


url = 'https://auto.ru/moskva/cars/{}/all/?page={}&output_type=list'


def parsePage(url, mark, pageNum):
	result = requests.get(url.format(mark, pageNum))
	soup = BeautifulSoup(result.content, 'html.parser')
	resultList = []
	carSelector = '.ListingItem-module__container'
	carsList = soup.select(carSelector)

	if len(carsList) == 0:
		return -1

	for car in carsList:
		resultRow = []

		resultRow.append(car.select_one('.Link.ListingItemTitle-module__link').text)
		try:
			resultRow.append(car.select_one('.ListingItemPrice-module__content').text)
		except Exception:
			resultRow.append(None)

		descr = car.select('.ListingItemTechSummaryDesktop__cell')[:3]

		for option in car.select('.ListingItemTechSummaryDesktop__cell'):
			resultRow.append(option.text)

		for i in range(3-len(descr)):
			resultRow.append(None)

		resultRow.append(car.select_one('.ListingItem-module__year').text)
		resultRow.append(car.select_one('.ListingItem-module__kmAge').text)

		# https://auto.ru/cars/used/sale/honda/civic/1095466368-4c049de6/
		# 1095466368-4c049de6

		link = car.select_one('.Link.ListingItemTitle-module__link').get('href')

		resultRow.append(link.split('/')[-2].split('-')[0])
		


		resultList.append(resultRow)

	return resultList

def writeToFile(dataList):
	with open('result.csv', 'a', encoding='utf8') as f:
		for row in dataList:
			writer = csv.writer(f)
			writer.writerow(row)


page = 30
while True:

	rowList = parsePage(url, 'honda', page)

	if rowList == -1:
		break

	writeToFile(rowList)
	print(page)
	page += 1
