#/home/fed/code/par_2/a06_team_db.py (ffe2a7e)

import os

from db_soc2 import insert_db, query_with_fetchall
""" добавление названия команд и относительных ссылок на них,
    авторов голов, раундов и коментариев
    из файлов в папке matchs/ в базу данных"""


def _work_db(query_1, query_2, data_tuple_list):
    # список таблицы комментариев
    pl_all = query_with_fetchall(query_1)
    # все ли комментарии есть в базе, если нет - вносим
    pl_list = []
    for p in data_tuple_list:
        if not (p in pl_all):
            pl_list.append(p)
    if len(pl_list) > 0:
        insert_db(query_2, pl_list)
        print('В базу внесено ', len(pl_list), ' позиций.')
        print(pl_list)


def _team_add(array):
    team = set()

    for r in array:
        if len(r) < 3:
            continue
        for i in [1, 3]:
            # относительная ссылка
            link_str_list = r[i+1].split('/')
            link = '/' + link_str_list[-3] + '/' + link_str_list[-2] + '/'
            # добавление кортежа название команд+ссылка
            team.add((r[i], link))

    # запрос на выборку всех команд
    query_1_1 = """ SELECT team_name_exp,team_url_exp FROM soc2.team; """
    # запрос на добавление команды
    query_2_1 = """INSERT INTO soc2.team (team_name_exp, team_url_exp) VALUES (%s,%s)"""

    _work_db(query_1_1, query_2_1, team)


def _goalscorer_add(array):
    # считываем из файла авторов голов
    player = set()

    for r in array:
        if len(r) < 3:
            continue
        a = 4
        # авторы голов хозяев
        while (not('gh' in r[a] and len(r[a]) == 3)):
            a += 1
        if r[a + 1] == 'Awarded':
            continue
        gols = int(r[a][-1])
        for j in range(gols):
            if r[a + j * 3 + 2] != '':
                player.add((r[a + j * 3 + 2],))
        # авторы голов гостей
        while (not('ga' in r[a] and len(r[a]) == 3)):
            a += 1
        if r[a + 1] == 'Awarded':
            continue
        gols = int(r[a][-1])
        for j in range(gols):
            if r[a + j * 3 + 2] != '':
                player.add((r[a + j * 3 + 2],))

    # запрос на выборку всех авторов голов
    query_1_2 = """ SELECT players_name FROM soc2.players; """

    # запрос на добавление автора гола
    query_2_2 = """INSERT INTO soc2.players (players_name) VALUES (%s)"""

    _work_db(query_1_2, query_2_2, player)


def _round_add(array):
    round_set = set()

    for r in array:
        if len(r) < 3:
            continue
        round_set.add((r[0],))

    # запрос на выборку всех авторов голов
    query_1_3 = """ SELECT round_name FROM soc2.round; """
    # запрос на добавление автора гола
    query_2_3 = """INSERT INTO soc2.round (round_name) VALUES (%s)"""

    _work_db(query_1_3, query_2_3, round_set)


def _comment_add(array):
    # считываем из файла авторов голов
    com = set()

    for r in array:
        if len(r) < 3:
            continue
        a = 4
        # авторы голов хозяев
        while (not('gh' in r[a] and len(r[a]) == 3)):
            a += 1
        if r[a + 1] == 'Awarded':
            continue
        gols = int(r[a][-1])
        for j in range(gols):
            if len(r[a + j * 3 + 2]) > 2:
                com.add((r[a + j * 3 + 3][1:-1],))
        # авторы голов гостей
        while (not('ga' in r[a] and len(r[a]) == 3)):
            a += 1
        if r[a + 1] == 'Awarded':
            continue
        gols = int(r[a][-1])
        for j in range(gols):
            if len(r[a + j * 3 + 2]) > 2:
                com.add((r[a + j * 3 + 3][1:-1],))

    # запрос на выборку комментариев
    query_1_4 = """ SELECT comment_text FROM soc2.comment; """
    # запрос на добавление комментария
    query_2_4 = """INSERT INTO soc2.comment (comment_text) VALUES (%s)"""

    _work_db(query_1_4, query_2_4, com)


def dop_match_add(file_one, country, player_bool=True, team_bool=True, round_bool=True, com_bool=True):
    file_name = 'matchs/%s/%s' % (country, file_one)

    with open(file_name) as f:
        array = [row.strip().split(';') for row in f]

    if player_bool == True:
        _goalscorer_add(array)

    if team_bool == True:
        _team_add(array)

    if round_bool == True:
        _round_add(array)

    if com_bool == True:
        _comment_add(array)


def __main__():
    file_one = ('veikkausliiga-2016.csv')
    country = 'finland'
    path = 'matchs/'
    if file_one == "all":
        for file_name in os.listdir(path + country + '/'):
            dop_match_add(file_name)
    else:
        dop_match_add(file_one, country)
    pass


if __name__ == "__main__":
    __main__()

