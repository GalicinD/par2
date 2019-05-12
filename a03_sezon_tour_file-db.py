#/home/fed/code/par_2/a03_sezon_tour_file-db.py (ffe2a7e)

import db_soc2


def len_poles(file_name='sezon_tour_list.csv'):
    """ определение длинны полей в файле вне зависимости от количества полей """

    len_pole = []
    with open(file_name, 'r') as f:
        for r in f:
            tour = r.rstrip().split(';')
            j = 0
            for i in tour:
                if len(len_pole) <= j:
                    len_pole.append(0)
                if len_pole[j] < len(i):
                    len_pole[j] = len(i)
                j += 1
    print(len_pole)


def sezon_insert_db(file_name='sezon_tour_list.csv'):
    """ функция добавления сезона из файла"""

    query1 = """INSERT INTO soc2.sezon (sezon_name) VALUES (%s)"""

    with open(file_name, 'r') as f:
        for r in f:
            r = db_soc2.not_unicod(r)
            sezon = str(r.rstrip().split(';')[0])
            query = "SELECT id_sezon FROM soc2.sezon where sezon_name=\'%s\';" % sezon
            if not db_soc2.query_with_fetchone(query):
                db_soc2.insert_one_row_db(query1, (sezon,))
                print(sezon)


def tour_insert_db(file_name='sezon_tour_list.csv'):
    """ функция добавления турниров из файла """

    flag_region = ""
    query2 = """INSERT INTO soc2.tournament(tournament_name, region_id_region)
        VALUES(%s,(SELECT id_region FROM soc2.region WHERE region_name=%s));"""

    with open(file_name, 'r') as f:
        for r in f:
            r = db_soc2.not_unicod(r)
            tour = r.rstrip().split(';')
            if flag_region != tour[2]:
                flag_region = tour[2]
                print(flag_region)
            query = """ SELECT id_tournament FROM soc2.tournament where tournament_name =\'%s\' and
                region_id_region=(SELECT id_region FROM soc2.region where region_name=\'%s\'); """ % (tour[1], tour[2])
            # добавление турниров
            if not db_soc2.query_with_fetchone(query):
                db_soc2.insert_one_row_db(query2, (tour[1], tour[2]))
                print((tour[1], tour[2]))


def tournament_sezon_insert_db(file_name='sezon_tour_list.csv'):
    """ функция добавления турниров по сезонам из файла"""

    flag_region = ""
    query3 = """INSERT INTO soc2.sezon_has_tournament
        (sezon_id_sezon,tournament_id_tournament,sezon_has_tournament_url_exp)
        value ((SELECT id_sezon FROM sezon WHERE sezon_name=%s),
        (SELECT id_tournament FROM tournament
        WHERE tournament_name=%s and region_id_region =
        (SELECT id_region FROM region WHERE region_name=%s)),
        %s);"""

    with open(file_name, 'r') as f:
        for r in f:
            r = db_soc2.not_unicod(r)
            tour = r.rstrip().split(';')
            if flag_region != tour[2]:
                flag_region = tour[2]
                print(flag_region)

            query = """ SELECT id_sezon_has_tournament FROM soc2.sezon_has_tournament where sezon_has_tournament_url_exp=\"%s\"; """ % tour[
                3]
            if not db_soc2.query_with_fetchone(query):
                db_soc2.insert_one_row_db(query3, tuple(tour))
                print(tour)


def __main():
    # определение длинны полей в файле вносимых в базу (не зависит от количества полей)
    len_poles()
    # добавление сезонов
    sezon_insert_db()
    # добавление турниров
    tour_insert_db()
    # добавление турниров с сезонами
    tournament_sezon_insert_db()


if __name__ == '__main__':
    __main()

