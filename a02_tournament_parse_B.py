#a02_tournament_parse_B.py

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
import re

import db_soc2

my_proxy = '172.104.43.148:8080'
url_base = 'https://www.betexplorer.com/soccer'
query4 = """ SELECT region_name,region_url_exp FROM soc2.region; """
driver = db_soc2.set_proxy(my_proxy)


def region_insert_db():
    global url_base, query4, driver
    data_country_list = db_soc2.query_with_fetchall(query4)

    driver.get(url_base)

    driver.find_element_by_css_selector(
        '#countries-select span').click()

    data1 = driver.find_element_by_id(
        'countries-select').find_elements_by_tag_name('a')

    reg_list = []
    for link in data1:
        country_tuple = (link.text, re.search(
            r'/soccer\S+', str(link.get_attribute('href'))).group()[7:])
        if not country_tuple in data_country_list:
            reg_list.append(country_tuple)
    print(reg_list)
    if reg_list:
        query = """INSERT INTO region
                (region_name,region_url_exp) 
                VALUES(%s,%s)"""
        db_soc2.insert_db(query, reg_list)


def query_toyr_seson(sezon_list, tour_list, tour_sezon_list):
        # добавление сезонов
    if sezon_list:
        query1 = """INSERT INTO soc2.sezon (sezon_name) VALUES (%s)"""
        db_soc2.insert_db(query1, sezon_list)

    # добавление турниров
    if tour_list:
        query2 = """INSERT INTO soc2.tournament(tournament_name, region_id_region)
            VALUES(%s,(SELECT id_region FROM soc2.region WHERE region_name=%s));"""
        db_soc2.insert_db(query2, tour_list)

    # сезон + турнир
    if tour_sezon_list:
        query3 = """INSERT INTO soc2.sezon_has_tournament
            (sezon_id_sezon,tournament_id_tournament,sezon_has_tournament_url_exp)
            value ((SELECT id_sezon FROM sezon WHERE sezon_name=%s),
            (SELECT id_tournament FROM tournament
            WHERE tournament_name=%s and region_id_region =
            (SELECT id_region FROM region WHERE region_name=%s)),
            %s);"""
        db_soc2.insert_db(query3, tour_sezon_list)


def tournament_sezon_insert_db(country_tuple):
    global url_base, driver

    url = url_base + country_tuple[1]
    driver.get(url)

    data1 = driver.find_elements_by_css_selector(
        ".h-text-left , .js-tablebanner-t a")
    sezon_list = []
    tour_list = []
    tour_sezon_list = []
    sezon = ''
    for i in data1:
        if i.get_attribute('href'):
            tour_link = re.search(
                r'/soccer\S+', str(i.get_attribute('href'))).group()[7:]
            query = "SELECT id_sezon_has_tournament FROM soc2.sezon_has_tournament where sezon_has_tournament_url_exp=\'%s\';" % tour_link
            if not db_soc2.query_with_fetchone(query):
                tour = i.text
                query = """ SELECT id_tournament FROM soc2.tournament where tournament_name =\'%s\' and
                    region_id_region=(SELECT id_region FROM soc2.region where region_name=\'%s\'); """ % (tour, country_tuple[0])
                if not db_soc2.query_with_fetchone(query) and not ((tour, country_tuple[0]) in tour_list):
                    tour_list.append((tour, country_tuple[0]))
                tour_sezon_tuple = (sezon, tour, country_tuple[0], tour_link)
                tour_sezon_list.append(tour_sezon_tuple)
        else:
            sezon = i.text
            query = "SELECT id_sezon FROM soc2.sezon where sezon_name=\'%s\';" % sezon
            if not db_soc2.query_with_fetchone(query):
                sezon_list.append((sezon,))
    # query_toyr_seson(sezon_list, tour_list, tour_sezon_list)
    write_csv(tour_sezon_list, 'sezon_tour_list.csv')


def write_csv(list, file_name):
    with open(file_name, 'a+') as f:
        for h in list:
            f.write(';'.join(h))
            f.write('\n')


def __main():
    global query4
    # region_insert_db()
    flag = True
    data_country_list = db_soc2.query_with_fetchall(query4)
    for j in data_country_list:
        if flag:
            tournament_sezon_insert_db(j)
            db_soc2.process_sleep(5)
        # if j[0] == 'Namibia':
        #     flag = True

    driver.close()
    driver.quit()


if __name__ == '__main__':
    __main()

