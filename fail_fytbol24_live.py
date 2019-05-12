#/home/fed/code/par_2/fail_fytbol24_live.py (ffe2a7e)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep


def __main():
    url = "https://www.betexplorer.com/soccer/"

    opts = Options()
    opts.set_headless()
    assert opts.headless  # без графического интерфейса.

    # driver = webdriver.Firefox(options=opts)
    driver = webdriver.Firefox()
    driver.get(url)

    data7 = driver.find_elements_by_class_name(
        'list-events__item__title')
    # '#countries-select .list-events__item__in')

    # data1 = soup.find(
    #     'div', class_="box-aside__section__in").findAll(
    #     "a", class_="list-events__item__title")
    reg_list = []
    for link in data7:
        reg_list.append((link.text, link.get_attribute("href")))
    print(reg_list)

    driver.quit()


if __name__ == '__main__':
    __main()

