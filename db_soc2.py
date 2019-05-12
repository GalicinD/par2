#/home/fed/code/par_2/db_soc2.py (ffe2a7e)

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from time import sleep

from mysql.connector import MySQLConnection, Error
from soc2_dbconfig import read_db_config


def set_proxy(my_proxy="2.39.150.215:8118", headless_bool=False):
    options = Options()
    if headless_bool:
        options.add_argument("--headless")

    proxy_host, proxy_port = my_proxy.split(':')

    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy_host)
    profile.set_preference("network.proxy.http_port", int(proxy_port))
    profile.update_preferences()
    return webdriver.Firefox(firefox_profile=profile, firefox_options=options)


def process_sleep(timer=1):
    sleep(timer)
    pass


def not_unicod(strings):
    if "'" in strings:
        strings = strings.replace("'", "''")
    if "ī" in strings:
        strings = strings.replace("ī", "i")
    if "ł" in strings:
        strings = strings.replace("ł", "l")
    return strings


def insert_db(query, data_list):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()

        cursor.executemany(query, data_list)
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def insert_one_row_db(query, args_tuple):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()

        cursor.execute(query, args_tuple)
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def query_with_fetchall(query):
    rows = None
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor(buffered=True)

        cursor.execute(query)

        rows = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return rows


def query_with_fetchone(query):
    row = None
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor(buffered=True)

        cursor.execute(query)

        row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return row


def main():
    pass


if __name__ == "__main__":
    main()

