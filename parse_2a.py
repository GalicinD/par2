#/home/fed/code/par_2/parse_2a.py (ffe2a7e)

from bs4 import BeautifulSoup
import requests
import fake_useragent
from time import sleep

# systemctl start tor.service
# pip3 install fake_useragent
# pip3 install bs4
# pip3 install requests
# pip3 install 'requests[socks]'


def gol_tab(a=0, b=1, c=2, d=0):
    gol = []
    global soup
    gol_list = []
    if int(gol[d]) > 0:
        data6 = soup.find('ul', class_="list-details list-details--shooters").findAll(
            'table', class_="table-main")[d].findAll('tr')
        for i in data6:
            min = i.findAll('td')[b].text[:-1]
            min = int(min.split("+")
                      [0]) + int(min.split("+")[1]) if "+" in min else int(min)
            gol_list.append((
                min,  # минута
                i.findAll('td')[c].text,  # игрок
                i.findAll('td')[a].text  # комент
            ))
    return gol_list


# Just a line
line = "---------------------------------------------------------------"

# Random User-Agent
ua = fake_useragent.UserAgent()
user = ua.random
header = {'User-Agent': str(user)}

# Connection to the ip-site
ipSite = 'http://icanhazip.com'
adress = requests.get(ipSite, headers=header)

# Check your ip adress
print(line + "\n[*] IP your network:\n"+adress.text + line)
print("[!] Connecting to the Tor network /", end="")

# Just points
for _ in range(5):
    sleep(0.2)
    print(end='.', flush=True)

# Proxie tor's
proxie = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Connecting to the network tor
try:
    adress = requests.get(ipSite, proxies=proxie, headers=header)

# Not connected
except:
    connection = False
    print("/\n[x] Stopping connect to the Tor network\n" + line)

# Connected
else:
    connection = True
    print("/\n[+] Connected to the Tor network\n" + line)
    print("[*] IP Tor network:\n" + adress.text + line)

# Parse site
finally:
    url = input("[!] Uniform Resource Locator:\n")

    if connection == True:
        page = requests.get(
            # "http://"+
            url.split()
            [0], proxies=proxie, headers=header)
    else:
        page = requests.get(
            # "http://" +
            url.split()[0], headers=header)

    soup = BeautifulSoup(page.text, "html.parser")
    # # Default parse - HTML
    # if url.split()[0] == url.split()[-1]:
    # 	with open("index.html","w") as html:
    # 		for tag in soup.findAll('html'):
    # 			html.write(str(tag))
    # 		print(line,"\nFile: 'index.html' created")
    # else:
    # 	# Parse tag
    # 	if url.split()[1] == url.split()[-1]:
    # 		for tag in soup.findAll(url.split()[1]):
    # 			print(tag)
    # 	# Parse inside/attribute
    # 	else:
    # 		if url.split()[2] == "inside":
    # 			for tag in soup.findAll(url.split()[1]):
    # 				print(tag.text)
    # 		else:
    # 			for tag in soup.findAll(url.split()[1]):
    # 				print(tag[url.split()[2]])
    # извлекаем страны
    print(soup)
    # data1 = soup.find('div', class_="international list").find(
    #     'ul', class_="countries").findAll('li')
    # # print(data1)
    # for link in data1:
    #     print(link.find('a').get_text(), link.find(
    #         'a').get('href'), link.get('data-id'))
    # извлекаем сезоны и соревнования в них
    # data2 = soup.find("table", class_="table-main js-tablebanner-t").findAll(
    #     "tbody")
    # data_dict = []
    # for blok in data2:
    #     sezon = blok.find("th", class_="h-text-left").get_text()
    #     range_list = blok.findAll("a")
    #     sor_list = []
    #     for link in range_list:
    #         sor_list.append((link.get_text(), link.get('href')))
    #     data_dict.append((sezon, sor_list))
    # извлекаем ссылки на матчи
    # data3 = soup.find(
    #     "table", class_="table-main h-mb15 js-tablebanner-t js-tablebanner-ntb").findAll("tr")
    # data_dict = []
    # kef_list = []
    # tyr = None
    # sor_list = []
    # for blok in data3:
    #     link = blok.find('td', class_="h-text-center")
    #     if link != None:
    #         sor_list.append((link.get_text(), link.find('a').get('href')))
    #     else:
    #         if tyr != None:
    #             data_dict.append((tyr, sor_list))
    #             print(tyr, ' ', sor_list, '\n', line)
    #             sor_list.clear
    #         # .get_text()
    #         tyr = blok.find("th").get_text()
    # извлекаем ссылки на будущие матчи
    # data4 = soup.find(
    #     "table", class_="table-main table-main--leaguefixtures h-mb15 js-tablebanner-t js-tablebanner-ntb").findAll("tr")
    # data_dict = []
    # tyr = None
    # sor_list = []
    # for blok in data4:
    #     link = blok.find('td', class_="h-text-left")
    #     if link != None:
    #         sor_list.append((link.findAll('span')[0].get_text(), link.findAll(
    #             'span')[0].get_text(), link.find('a').get('href'), blok.find(
    #             'td', class_="table-main__datetime").get_text()))
    #     else:
    #         if tyr != None:
    #             data_dict.append((tyr, sor_list))
    #             print(tyr, ' ', sor_list, '\n', line)
    #             sor_list.clear
    #         # .get_text()
    #         tyr = blok.find("th").get_text()
    # обработка страницы матча
    # хозяева гости
    # data5 = soup.find('ul', class_="list-details").findAll(
    #     'li', class_="list-details__item")
    # team_list = []
    # for team in data5:
    #     if team.find('a') != None:
    #         team_list.append((team.find('h2', class_="list-details__item__title").text,
    #                           team.find('a').get('href')))
    # print(team_list)
    # голы минуты коменты
    # data_gol = soup.find('ul', class_="list-details").findAll(
    #     'li', class_="list-details__item")[1].find('p', class_="list-details__item__score").text
    # gol = data_gol.split(':')
    # print(data_gol)
    # print(gol_tab())
    # print(gol_tab(2, 0, 1, 1))

    # data_dict = []
    # tyr = None
    # sor_list = []
    # for blok in data4:
    #     link = blok.find('td', class_="h-text-left")
    #     if link != None:
    #         sor_list.append((link.findAll('span')[0].get_text(), link.findAll(
    #             'span')[0].get_text(), link.find('a').get('href'), blok.find(
    #             'td', class_="table-main__datetime").get_text()))
    #     else:
    #         if tyr != None:
    #             data_dict.append((tyr, sor_list))
    #             print(tyr, ' ', sor_list, '\n', line)
    #             sor_list.clear
    #         # .get_text()
    #         tyr = blok.find("th").get_text()

    # print(data_dict, line)


# import scrapy


# from scrapy.crawler import CrawlerProcess


# class PythonEventsSpider(scrapy.Spider):
#     name = 'pythoneventsspider'
#     start_urls = ['https://www.betexplorer.com/soccer/']

#     country_list = []

#     def parse(self, response):
#         global country_list
#         name_list = []
#         url_list = []
#         name_list = response.css(
#             '#countries-select .list-events__item__title *::text').getall()
#         url_list = response.css(
#             '#countries-select .list-events__item__title *::attr(href)').getall()
#         for i in range(0, len(name_list)):
#             country_list.append((name_list[i], url_list[i]))

#     print(country_list)


# if __name__ == "__main__":
#     process = CrawlerProcess({'LOG_LEVEL': 'ERROR'})
#     process.crawl(PythonEventsSpider)
#     spider = next(iter(process.crawlers)).spider
#     process.start()

