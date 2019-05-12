from random import randint
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import re
import os
import gc

from db_soc2 import query_with_fetchall, set_proxy, process_sleep

my_proxy = "217.113.122.142:3128"


def _read_link(country, liga):
    link_match = []

    file_name = 'tourn/%s/web_match_%s.csv' % (country, liga)
    with open(file_name) as f:
        array = [row.strip().split(';') for row in f]
    for r in array:
        if len(r) == 1:
            continue
        for i in range(2, len(r), 2):
            link_match.append(r[i])
            link_match.append(r[0])
    return link_match


def _match_rospis(country, liga):
    line = "---------------------------------------------------------------"
    global my_proxy
    gol_away_list = []
    gol_home_list = []
    kef_list = []
    match_data_list = []

    file_rez = 'matchs/%s/%s.csv' % (country, liga)

    # из файла получаем список ссылок на матчи
    link_match = _read_link(country, liga)
    end = int(len(link_match) / 2)

    driver = set_proxy(my_proxy)
    count_p = 0

    for p in range(end):
        # проверка -парсился ли матч по данной ссылке, есть ли ссылка в файле и/или базе
        try:
            with open(file_rez) as f:
                if re.search(r'/[^/]*/[^/]*/[^/]*/[^/]*/$', link_match[p*2]).group() in f.read():
                    continue
        except AttributeError:  # не найти "re" выражения в строке  которая должна быть ссылкой
            pass
        except FileNotFoundError:  # если нет файла, в который парсится турнир
            pass
        # перегружаем вебдрайвер, чтоб он не разросся на всю оперативку
        count_p += 1
        if count_p > 70:
            driver.close()
            driver.quit()
            driver = set_proxy(my_proxy)
            count_p = 0

        driver.get(link_match[p * 2])
        process_sleep(2)

        # 0 - раунд
        match_data_list.append(link_match[p * 2 + 1])
        try:
            # 1- команда хозяев
            match_data_list.append(driver.find_element_by_xpath(
                '/html/body/div[4]/div[4]/div/div/div[1]/section/ul[2]/li[1]/h2/a').text)
            # 2 - относительная ссылка на команду хозяев
            match_data_list.append(re.search(r'/[^/]*/[^/]*/$', driver.find_element_by_xpath(
                '/html/body/div[4]/div[4]/div/div/div[1]/section/ul[2]/li[1]/h2/a').get_attribute("href")).group())
            # 3 - гости
            match_data_list.append(driver.find_element_by_xpath(
                '/html/body/div[4]/div[4]/div/div/div[1]/section/ul[2]/li[3]/h2/a').text)
            # 4 - относительная ссылка на команду гостей
            match_data_list.append(re.search(r'/[^/]*/[^/]*/$', driver.find_element_by_xpath(
                '/html/body/div[4]/div[4]/div/div/div[1]/section/ul[2]/li[3]/h2/a').get_attribute("href")).group())
        except NoSuchElementException:
            # 1- команда хозяев
            match_data_list.append(driver.find_element_by_xpath(
                '/html/body/div[3]/div[4]/div/div/div[1]/section/ul[2]/li[1]/h2/a').text)
            # 2 - относительная ссылка на команду хозяев
            match_data_list.append(re.search(r'/[^/]*/[^/]*/$', driver.find_element_by_xpath(
                '/html/body/div[3]/div[4]/div/div/div[1]/section/ul[2]/li[1]/h2/a').get_attribute("href")).group())
            # 3 - гости
            match_data_list.append(driver.find_element_by_xpath(
                '/html/body/div[3]/div[4]/div/div/div[1]/section/ul[2]/li[3]/h2/a').text)
            # 4 - относительная ссылка на команду гостей
            match_data_list.append(re.search(r'/[^/]*/[^/]*/$', driver.find_element_by_xpath(
                '/html/body/div[3]/div[4]/div/div/div[1]/section/ul[2]/li[3]/h2/a').get_attribute("href")).group())
        # 5 - дата время
        match_data_list.append(driver.find_element_by_id('match-date').text)

        # 6 - URL матча (относительное)
        match_data_list.append(
            re.search(r'/[^/]*/[^/]*/[^/]*/[^/]*/$', str(link_match[p*2])).group())

        # 7 - счёт
        match_data_list.append(driver.find_element_by_id('js-score').text)

        try:
            if driver.find_element_by_id('js-eventstage').text == 'Awarded':
                if match_data_list[7] == '3:0':
                    gol_home_list.append('Awarded')
                else:
                    gol_away_list.append('Awarded')
            elif driver.find_element_by_id('js-eventstage').text == 'Canceled':
                gol_home_list.append('Canceled')
        except:
            # голы хозяева: минуты-игроки-комент(если есть)
            if int(match_data_list[7][: match_data_list[7].find(':')]) > 0:
                min_list = driver.find_elements_by_css_selector(
                    '.list-details__item:nth-child(1) td:nth-child(2)')
                player_list = driver.find_elements_by_css_selector(
                    '.list-details__item:nth-child(1) td~ td+ td')
                com_list = driver.find_elements_by_css_selector(
                    '.list-details__item:nth-child(1) td:nth-child(1)')
                for k in range(int(match_data_list[7][: match_data_list[7].find(':')])):
                    try:
                        gol_home_list.append(min_list[k].text)
                        gol_home_list.append(player_list[k].text)
                        gol_home_list.append(com_list[k].text)
                    except IndexError:
                        gol_home_list.append('90')
                        gol_home_list.append('unknown')
                        gol_home_list.append('')

            # голы гости: минуты-игроки-комент(если есть)
            if int(match_data_list[7][match_data_list[7].find(':')+1:]) > 0:
                min_list = driver.find_elements_by_css_selector(
                    '.list-details__item+ .list-details__item td:nth-child(1)')
                player_list = driver.find_elements_by_css_selector(
                    '.list-details__item+ .list-details__item td:nth-child(2)')
                com_list = driver.find_elements_by_css_selector(
                    '.list-details__item+ .list-details__item td~ td+ td')
                for k in range(int(match_data_list[7][match_data_list[7].find(':')+1:])):
                    try:
                        gol_away_list.append(min_list[k].text)
                        gol_away_list.append(player_list[k].text)
                        gol_away_list.append(com_list[k].text)
                    except IndexError:
                        gol_away_list.append('90')
                        gol_away_list.append('unknown')
                        gol_away_list.append('')

        # кефы 1х2
        kef_list.append('av1x2')
        try:
            data1 = driver.find_elements_by_css_selector(
                '#match-add-to-selection .table-main__detail-odds')
            for u in data1:
                kef_list.append(u.text)

            data1 = driver.find_element_by_id(
                'odds-content').find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            i = 1
            for blok in data1:
                if blok.get_attribute('data-bid') in ['18', '44']:
                    kef_list.append(blok.get_attribute('data-bid') + '1x2')
                    for k in [4, 5, 6]:
                        st = str(i)+']/td['+str(k)
                        kef_list.append(driver.find_element_by_xpath(
                            '//*[@id="sortable-1"]/tbody/tr[%s]/span' % st).text)
                i += 1
            # нажать б/м и кефы б/м
            driver.find_element_by_css_selector(
                '.list-tabs__item:nth-child(2) .list-tabs__item__in').click()

            process_sleep(2)
            data1 = driver.find_elements_by_css_selector(
                '.odd:nth-child(1) .table-main__doubleparameter')
            for j in range(len(data1)):
                sortable = str(data1[j].text)
                if not (sortable in ['0.5', '1.5', '2.5', '3.5']):
                    continue

                data2 = driver.find_elements_by_css_selector(
                    '#sortable-%s #match-add-to-selection .table-main__detail-odds' % str(j + 1))

                kef_list.append('avou%s' % sortable)
                kef_list.append(data2[0].get_attribute('data-odd'))
                kef_list.append(data2[1].get_attribute('data-odd'))
                i = 1

                data2 = driver.find_element_by_id(
                    'sortable-%s' % str(j + 1)).find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
                for blok in data2:
                    if blok.get_attribute('data-bid') in ['18', '44']:
                        kef_list.append(blok.get_attribute(
                            'data-bid') + 'ou' + sortable)
                        st = '%s"]/tbody/tr[%s' % (str(j + 1), str(i))
                        try:
                            kef_list.append(driver.find_element_by_xpath(
                                '//*[@id="sortable-%s]/td[5]/span' % st).text)
                        except:
                            kef_list.append('')
                        try:
                            kef_list.append(driver.find_element_by_xpath(
                                '//*[@id="sortable-%s]/td[6]/span' % st).text)
                        except:
                            kef_list.append('')

                    i += 1
                data2 = None
            data1 = None
        except WebDriverException as err:
            print(err)

        match_data_list.append('gh%s' % match_data_list[7].split(":")[0])
        match_data_list = match_data_list + gol_home_list
        match_data_list.append('ga%s' % match_data_list[7].split(":")[-1])
        match_data_list = match_data_list + gol_away_list
        match_data_list = match_data_list + kef_list

        # print(match_data_list)
        with open(file_rez, 'a') as fr:
            fr.write(';'.join(match_data_list))
            fr.write('\n')
        print(p+1, '(', end, ')',
              match_data_list[1], ' - ', match_data_list[3], match_data_list[6])
        print(match_data_list[7], match_data_list[5])
        print(gol_home_list)
        print(gol_away_list)
        print(kef_list)
        print(match_data_list[0])
        print(line)

        gol_home_list.clear()
        gol_away_list.clear()
        kef_list.clear()
        match_data_list.clear()
        # чистим память
        gc.collect()

        # process_sleep(randint(5, 10))
    driver.close()
    driver.quit()


def _link_st(data1, country, liga, flag='rezults'):
    file_csv = 'tourn/%s/web_match_%s.csv' % (country, liga)
    str_csv_list = []
    flag_bool = True

    with open(file_csv, "a+") as web_match_csv:
        for blok in data1:
            try:
                var_str = blok.find_element_by_tag_name(
                    'a').get_attribute('href')
                if flag_bool:
                    str_csv_list.append(flag)
                    flag_bool = False
                if not (var_str in web_match_csv.read()):
                    str_csv_list.append(
                        blok.find_element_by_tag_name('a').text)
                    str_csv_list.append(var_str)
            except WebDriverException as err:
                if len(str_csv_list) > 1:
                    web_match_csv.write((';').join(str_csv_list))
                    web_match_csv.write('\n')
                str_csv_list.clear()
                str_csv_list.append(blok.text)
                flag_bool = False
        if len(str_csv_list) > 1:
            web_match_csv.write((';').join(str_csv_list))
            web_match_csv.write('\n')


def _results_match(country, liga, end_url):
    global my_proxy
    url = 'https://www.betexplorer.com/soccer/%s/%s%s' % (
        country, liga, end_url)

    driver = set_proxy(my_proxy)
    driver.get(url)
    # try:
    # нажимаем кнопки, перебирая стадии
    data2 = driver.find_elements_by_css_selector(
        '#sm-0-0 .list-tabs__item__in')
    if data2:
        for i in range(len(data2)):
            var = driver.find_element_by_xpath(
                '//*[@id="sm-0-0"]/div/ul/li[%s]/a' % str(i + 1)).text
            href = driver.find_element_by_xpath(
                '//*[@id="sm-0-0"]/div/ul/li[%s]/a' % str(i + 1)).get_attribute('href')
            driver.get(href)

            data1 = driver.find_elements_by_css_selector('.h-text-left')
            _link_st(data1, country, liga, var)
    else:
        # если кнопок нет и одна стадия
        data1 = driver.find_elements_by_css_selector('.h-text-left')
        _link_st(data1, country, liga)

    driver.close()
    driver.quit()


def match_parse(country, liga, url_end='',  results_match_bool=True):
    # если нет папок страны -создаём
    if not (os.path.exists('matchs/%s/' % country)):
        os.mkdir('matchs/%s/' % country)
    if not (os.path.exists('tourn/%s/' % country)):
        os.mkdir('tourn/%s/' % country)

    file_rez = 'tourn/%s/web_match_%s.csv' % (country, liga)

    if results_match_bool:
        # нужно ли искать ссылки на матчи
        _results_match(country, liga, url_end)
    # сканируем матчи и заносим данные в файл
    _match_rospis(country, liga)


def __main():
    url_end = "/results/"

    # country = 'england'
    # liga = 'league-one-2017-2018'

    # match_parse(country, liga, url_end, href_match_bool=True,
    #             results_match_bool=True)

    query_3_1 = """ SELECT sezon_has_tournament_url_exp FROM soc2.sezon_has_tournament
        where sezon_has_tournament_url_exp like '%/ireland/premier-division-%' and
        (sezon_has_tournament_url_exp like '%2018/%'
        or sezon_has_tournament_url_exp like '%2017/%'
        or sezon_has_tournament_url_exp like '%2016/%'
        or sezon_has_tournament_url_exp like '%2015/%'
        or sezon_has_tournament_url_exp like '%2014/%'
        or sezon_has_tournament_url_exp like '%2013/%'
        ); """

    tour_list_href = query_with_fetchall(query_3_1)
    # print(tour_list_href)

    for h in tour_list_href:
        country = h[0].split('/')[1]
        liga = h[0].split('/')[2]
        match_parse(country, liga, url_end,
                    results_match_bool=True)


if __name__ == '__main__':
    __main()
