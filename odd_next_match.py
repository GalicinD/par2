#/home/fed/code/par_2/odd_next_match.py (ffe2a7e)

from random import randint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import datetime


def cicle(url, date_str):
    file_name = 'test_text.txt'

    driver = webdriver.Firefox()
    driver.get(url)

    sleep(20)
    # while (1):
    sl = 20
    with open(file_name, 'r') as f:
        cod_file = f.read()
        exec(cod_file)

    file_rez = 'fav_' + date_str + '.csv'
    f1 = open(file_rez, 'w')
    f1.close
    with open(file_rez, 'a') as fr:
        kef = []
        match_time = []
        match_title = []
        score = []
        score = driver.find_elements_by_css_selector(
            '.table-score')
        kef = driver.find_elements_by_css_selector('.odds-nowrp')
        match_title = driver.find_elements_by_css_selector(
            '.table-participant a')
        match_time = driver.find_elements_by_css_selector(
            '.datet')
        print('kef=', len(kef),
              'match_title=', len(match_title), 'match_time=', len(match_time))
        for a in match_title:
            if len(a.text) < 10:
                match_title.remove(a)
        print('kef=', len(kef),
              'match_title=', len(match_title), 'match_time=', len(match_time))
        for i in range(len(match_time)):
            try:
                if float(kef[i * 3 + 2].get_attribute('xodd')) < float(kef[i * 3].get_attribute('xodd')) and float(kef[i * 3 + 2].get_attribute('xodd')) > 1.49:
                    if len(score) > i:
                        sc = score[i].text
                    else:
                        sc = '-:-'
                    # print(match_time[i].text,
                    #       match_title[i].text, kef[i*3].get_attribute('xodd'), kef[i*3+2].get_attribute('xodd'), '\n')
                    str_write = match_time[i].text + ';' + sc + ';' + match_title[i].text + ';' + kef[i * 3].get_attribute(
                        'xodd') + ';' + kef[i * 3 + 1].get_attribute('xodd') + ';' + kef[i * 3 + 2].get_attribute('xodd')
                    print(str_write)
                    str_write = str_write + \
                        ';' + match_title[i].get_attribute("href") + '\n'
                    fr.write(str_write)
            except:
                continue
        print('End')
        # for t in range(sl):
        #     sleep(1)
        #     print(end='.', flush=True)
    driver.quit()


def __main():
    url_base = "https://www.oddsportal.com/matches/soccer/"
    date_str = '{0:%Y%m%d}'.format(
        datetime.date.today() + datetime.timedelta(days=-1))
    url = url_base + date_str + '/'
    cicle(url, date_str)


if __name__ == '__main__':
    __main()

