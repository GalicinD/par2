# /home/fed/code/par_2/a05_match_db.py (ffe2a7e)

import os
import re
from datetime import datetime

from a06_team_db import dop_match_add
from a07_gol_db import gol_add
from db_soc2 import insert_db, query_with_fetchone, insert_one_row_db
""" добавление матчей
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


def _match_db(file_name, country):
    # запрос на выборку матчей по ссылке
    query_1_5 = "SELECT id_match FROM soc2.match WHERE match_url_exp="
    # запрос на добавление матча
    query_2_5 = """INSERT INTO soc2.match
        (match_home, match_away, match_tour, match_round,match_datatime,
        match_url_exp, match_k_av_1, match_k_av_x, match_k_av_2,
        match_k_18_1, match_k_18_x, match_k_18_2, match_k_44_1,
        match_k_44_x, match_k_44_2, m_k_av_o_05, m_k_av_u_05, m_k_av_o_15,
        m_k_av_u_15, m_k_av_o_25, m_k_av_u_25, m_k_av_o_35, m_k_av_u_35,
        m_k_18_o_05, m_k_18_u_05, m_k_18_o_15, m_k_18_u_15, m_k_18_o_25,
        m_k_18_u_25, m_k_18_o_35, m_k_18_u_35, m_k_44_o_05, m_k_44_u_05,
        m_k_44_o_15, m_k_44_u_15, m_k_44_o_25, m_k_44_u_25, m_k_44_o_35, m_k_44_u_35,
        match_status)
        value ((SELECT id_team FROM team WHERE team_name_exp=%s),
        (SELECT id_team FROM team WHERE team_name_exp=%s),
        (SELECT id_sezon_has_tournament FROM sezon_has_tournament
        WHERE sezon_has_tournament_url_exp LIKE %s)
        ,(SELECT id_round FROM round WHERE round_name=%s),%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,
        (SELECT id_status FROM status WHERE status_name=%s));"""
    match_list = []
    tuple_match = []
    href_match = []

    print('--------------------------------------------------------')
    print('Обрабатывается файл: matchs/%s/%s' % (country, file_name))

    with open('matchs/%s/%s' % (country, file_name)) as f:
        array = [row.strip().split(';') for row in f]

    # если разделение идёт по знакам табуляции
    if len(array[0]) == 1:
        array0 = [row[0].strip().split('\t') for row in array]
        array = array0
        array0.clear

    # если нет прямой ссылки на матч извлекаем из файла web_match_
    if not array[1][6].startswith('https'):
        href_match = _read_link(file_name, country)

    # если необходимо вносим игроков,команды,раунды и комменты
    dop_match_add(file_name, country)

    for r in array:
        # избавляемся от мусорных строк
        if len(r) < 3:
            continue
        # определяем ссылку на матч
        if len(href_match) > 1:
            link = href_match[r[0] +
                              r[2].split('/')[-3] + '-' + r[4].split('/')[-3]]
        else:
            if len(r[6].split('/')) > 4:
                link = re.search(r'/[^/]*/[^/]*/[^/]*/[^/]*/$', r[6]).group()
            else:
                link = '/%s/%s%s' % (country, file_name[:-4], r[6])

        # проверка по ссылке наличия дубликатов-матчей в базе
        if query_with_fetchone(query_1_5 + "\'" + link + "\'") != None:
            continue
        if any("Awarded" in s for s in r):
            status = 'Awarded'
        elif any("Canceled" in s for s in r):
            status = 'Canceled'
        else:
            status = 'finished'
        # проверка по ссылке наличия дубликатов-матчей в обрабатываемом файле
        flag = False
        for l in match_list:
            if l[5] == link:
                flag = True
                break
        if flag:
            continue

        # 0-1: хозяева(1) и гости (2)
        tuple_match.append(r[1])
        tuple_match.append(r[3])
        # 2 - название файла для определения турнира+сезона
        tuple_match.append('%/'+country+'/' + file_name[:-4]+'/%')
        # 3 раунд
        tuple_match.append(r[0])
        # 4 дата и время
        a = 5
        if len(r[a]) < 10:
            d = '01.01.1901 - 01:00'
        elif len(r[a]) < 17 and r[a+1][:4] != 'https':
            d = r[a] + r[a+1]
        else:
            d = r[a]
        datetime_object = datetime.strptime(d, '%d.%m.%Y - %H:%M')
        tuple_match.append(datetime_object)

        # 5 - ссылка на матч
        tuple_match.append(link)

        # добавляем кефы
        while (not('av1x2' == r[a])):
            a += 1
        for d in ['av1x2', '181x2', '441x2']:
            if len(r) > a and r[a] == d:
                for i in range(3):
                    try:
                        tuple_match.append(float(r[i + a + 1]))
                    except ValueError:
                        tuple_match.append(None)
                    except IndexError:
                        tuple_match.append(None)
                a += 4
            else:
                for i in range(3):
                    tuple_match.append(None)

        for d in ['avou0.5', '18ou0.5', '44ou0.5', 'avou1.5', '18ou1.5',
                  '44ou1.5', 'avou2.5', '18ou2.5', '44ou2.5', 'avou3.5', '18ou3.5', '44ou3.5']:
            if a < len(r) and r[a] == d:
                for i in range(2):
                    try:
                        tuple_match.append(float(r[i + a + 1]))
                    except ValueError:
                        tuple_match.append(None)
                a += 3
            else:
                for i in range(2):
                    tuple_match.append(None)
        tuple_match.append(status)

        try:
            insert_one_row_db(query_2_5, tuple(tuple_match))
        except:
            print('Error: s', tuple_match)
        # match_list.append(tuple(tuple_match))
        if len(tuple_match) != 40:
            print(len(tuple_match))
            print(tuple_match)

        tuple_match.clear()

    # print(match_list)
    # insert_db(query_2_5, match_list)

    # добавляем голы
    gol_add(file_name, country, False)


def match_add(file_one, country):
    path = 'matchs/'
    if file_one[-4:] == '.csv':
        _match_db(file_one, country)
    elif file_one == "all":
        for file_name in os.listdir('%s%s/' % (path, country)):
            _match_db(file_name, country)
    else:
        for file_name in os.listdir('%s%s/' % (path, country)):
            if file_one in file_name:
                _match_db(file_name, country)


def __main__():
    file_one = ('all')
    country = 'belarus'
    match_add(file_one, country)
    pass


if __name__ == "__main__":
    __main__()

