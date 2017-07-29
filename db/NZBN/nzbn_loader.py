import psycopg2
import os
from config import config


def executeSQL(conn, sql):
    print sql
    # create a cursor
    cur = conn.cursor()
    # execute a statement
    cur.execute(sql)
    # close the communication with the PostgreSQL
    cur.close()


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        readfiles(conn)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def getElement(startPattern, data, endPattern):
    start = data.find(startPattern)
    start += len(startPattern)
    end = data.find(endPattern, start)
    return data[start:end]


def processDirector(cid, conn, data):
    firstName  = getElement(r'FirstName">', data, '<')
    MiddleName = getElement(r'MiddleName">', data, '<')
    LastName   = getElement(r'LastName">', data, '<')

    insertDirector = "INSERT INTO nzbn_director values (%s,'%s','%s','%s')" % (cid, firstName, MiddleName, LastName)
    executeSQL(conn, insertDirector)


def getDelimitedSections(cid, conn, str, delimiter):
    remaining = len(str)
    if 0 == remaining:
        return None
    dlength = len(delimiter)
    start = str.find(delimiter)
    if (-1) == start:
        return None
    start += + dlength
    end = str.find(delimiter, start)
    processDirector(cid, conn, str[start:end])
    end += dlength
    getDelimitedSections(cid, conn, str[end:],delimiter)

def getCompany(xmldata, conn):
    cid = getElement(r'PartyID="',xmldata,'"')
    name = getElement(r'N2:ElementType="FullName">',xmldata,'<')
    insertCompany = "INSERT INTO nzbn_business values (%s,'%s')" % (cid, name)
    executeSQL(conn, insertCompany)
    return cid

def getDirectors(xmldata, cid, conn):
    getDelimitedSections(cid, conn, xmldata,'N1:Director')

def readonefile(f, conn):
    fpath = "/Users/steven/Downloads/nzbn-bulk/%s" % f
    with open(fpath, 'r') as myfile:
        xmldata = myfile.read().replace('\n', '')
        cid = getCompany(xmldata, conn)
        getDirectors(xmldata, cid, conn)
        executeSQL(conn,"COMMIT")

def readfiles(conn):
    indir = '/Users/steven/Downloads/nzbn-bulk'
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            readonefile(f, conn)

if __name__ == '__main__':
    connect()