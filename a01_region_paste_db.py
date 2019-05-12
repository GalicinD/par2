#a01_region_paste_db.py

from mysql.connector import MySQLConnection, Error
from soc2_dbconfig import read_db_config
from start import connect_tor


def insert_region(reg_list):
    query = """INSERT INTO region
               (region_name,region_url_exp) 
               VALUES(%s,%s)"""

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        # for reg in reg_list:
        cursor.executemany(query, reg_list)

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def __main():
    url = "https://www.betexplorer.com/soccer/"
    soup = connect_tor(url)
    data1 = soup.find(
        'div', class_="box-aside__section__in").findAll(
        "a", class_="list-events__item__title")
    reg_list = []
    for link in data1:
        reg_list.append((link.get_text(), link.get('href')))
    print(reg_list)
    insert_region(reg_list)


if __name__ == '__main__':
    __main()

