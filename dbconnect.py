import MySQLdb


def connection():
    conn = MySQLdb.connect(host='127.0.0.1',
                           port=3306,
                           user='bluegarden',
                           passwd='XN4rcpxxwXdcDm2E',
                           db='bluegarden')

    c = conn.cursor()
    return c, conn
