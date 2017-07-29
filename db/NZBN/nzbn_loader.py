import psycopg2
import os
from govhack.config import config
from xml.etree import ElementTree
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

def processDirector(data):
    print data
    firstName = re.match(r'N2:ElementType="FirstName">(.+?)\<\/N',data)
    print firstName.group()

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
        xmldata = '<root>' + myfile.read().replace('\n', '') + '</root>'
        getDirectors(xmldata)

def readfiles():
    indir = '/Users/steven/Downloads/nzbn-bulk'
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            readonefile(f)

if __name__ == '__main__':
    readonefile('/Users/steven/Downloads/nzbn-bulk/companyaaana')