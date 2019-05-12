# /home/fed/code/par_2/a07_gol_db.py (ffe2a7e)

import os
import re
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from soc2_dbconfig import read_db_config

from db_soc2 import insert_db, query_with_fetchone, query_with_fetchall
from a06_team_db import dop_match_add
""" добавление авторов голов
    из файлов в папке matchs/ в базу данных"""


def _read_link(file_name, country):
    link_match = {}

    file_n = 'tourn/%s/web_match_%s' % (country, file_name)
    with open(file_n) as f:
        array = [row.strip().split(';') for row in f]
    for r in array:
        if len(r) == 1:
            continue
        for i in range(2, len(r), 2):
            link_match[r[0]+r[i].split('/')[-3]
                       ] = re.search(r'/[^/]*/[^/]*/[^/]*/[^/]*/$', r[i]).group()
    return link_match


def gol_add(file_name, country, dop_bool=True):
    # запрос на голы в матче по ссылке(поиск дубликатов в базе)
    query_1_6 = """SELECT gol_time,
        (select players_name from players where id_players = gol.gol_player),
        (select comment_text from comment where id_comment = gol.gol_com), 
        gol_home FROM soc2.gol 
        WHERE gol_match=(SELECT id_match FROM soc2.match WHERE match_url_exp="""
    # запрос на добавление матча
    query_2_6 = """INSERT INTO soc2.gol
        (gol_match, gol_time, gol_player, gol_com, gol_home)
        value ((SELECT id_match FROM soc2.match
        WHERE match_url_exp =%s),%s,
        (SELECT id_players FROM players WHERE players_name=%s),
        (SELECT id_comment FROM soc2.comment WHERE comment_text=%s),%s
        );"""

    gol_list = []
    gol_db = []

    with open('matchs/%s/%s' % (country, file_name)) as f:
        array = [row.strip().split(';') for row in f]

    # для поиска ссылки на матч надо обработать файл web_match_
    if array[1][6][:4] != 'https':
        href_match = _read_link(file_name, country)

    for r in array:
        if len(r) < 3:
            continue
        # ссылка на матч
        if len(href_match) > 1:
            link = href_match[r[0] +
                              r[2].split('/')[-3] + '-' + r[4].split('/')[-3]]
        else:
            link = '/' + r[6].split('/')[-3] + '/' + \
                r[6].split('/')[-2] + '/'
        # выбираем из базы все голы для этого матча по ссылке
        gol_db = query_with_fetchall(query_1_6 + "\'" + link + "\')")
        # авторы голов хозяев
        a = 4
        for g in ['gh', 'ga']:
            while (not(g in r[a] and len(r[a]) in [3, 4])):
                a += 1
            if not(r[a + 1] in ['Awarde', 'Awarded']):
                for j in range(int(r[a][2:])):
                    # минута гола
                    if r[a + 1][:1] in ['ga', 'av']:
                        break
                    elif '+' in r[a + 1]:
                        minuta = int(r[a + 1][:-1].split('+')[0]) * \
                            100 + int(r[a + 1][:-1].split('+')[1])
                    else:
                        minuta = int(r[a + 1][:-1])
                    # забивший гол
                    if r[a + 2] != '':
                        pl = r[a + 2]
                    else:
                        pl = 'unknown'

                    # комментарий
                    if len(r[a + 3]) == 0:
                        com = None
                    else:
                        com = r[a + 3][1:-1]

                    # кто забил
                    gol_home = 1 if g == 'gh' else 0

                    if not ((minuta, pl, com, gol_home) in gol_db):
                        gol_list.append((link, minuta, pl, com, gol_home))
                        print(link, minuta, pl, com, gol_home)
                    a += 3
        # print(gol_db)
        try:
            gol_db.clear
        except AttributeError:
            pass

    # все ли авторы есть в базе, если нет - вносим если надо
    if dop_bool:
        dop_match_add(file_name, country)

    # print(gol_list)
    insert_db(query_2_6, gol_list)


def __main__():
    file_one = ('all')
    country = 'belarus'
    path = 'matchs/'

    if file_one == "all":
        for file_name in os.listdir('%s%s/' % (path, country)):
            gol_add(file_name, country)
    elif file_one[-4:] != '.csv':
        for file_name in os.listdir('%s%s/' % (path, country)):
            if file_one in file_name:
                gol_add(file_name, country)
    else:
        gol_add(file_one, country)
    pass


if __name__ == "__main__":
    __main__()

