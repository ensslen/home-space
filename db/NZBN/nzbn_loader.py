import psycopg2
import os
from config import config
import re


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

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def getElement(pattern, data):
    start = data.find(pattern)
    start += len(pattern)
    end = data.find(r'<', start)
    return data[start:end]


def processDirector(data):
    firstName  = getElement(r'FirstName">', data)
    MiddleName = getElement(r'MiddleName">', data)
    LastName   = getElement(r'LastName">', data)

    print firstName
    print MiddleName
    print LastName


def getDelimitedSections(str, delimiter):
    remaining = len(str)
    if 0 == remaining:
        return None
    dlength = len(delimiter)
    start = str.find(delimiter)
    if (-1) == start:
        return None
    start += + dlength
    end = str.find(delimiter, start)
    processDirector( str[start:end])
    end += dlength
    getDelimitedSections(str[end:],delimiter)

def getDirectors(xmldata):
    getDelimitedSections(xmldata,'N1:Director')

def readonefile(f):
    #xmldoc = minidom.parse('/Users/steven/Downloads/nzbn-bulk/companyaaana')
    with open(f, 'r') as myfile:
        xmldata = myfile.read().replace('\n', '')
        getDirectors(xmldata)

def readfiles():
    indir = '/Users/steven/Downloads/nzbn-bulk'
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            readonefile(f)

if __name__ == '__main__':
    readonefile('/Users/steven/Downloads/nzbn-bulk/companyaaana')