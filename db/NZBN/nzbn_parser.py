import os


def getElement(startPattern, data, endPattern):
    start = data.find(startPattern)
    start += len(startPattern)
    end = data.find(endPattern, start)
    return data[start:end].replace('"',"'")


def processDirector(cid, f, data):
    firstName  = getElement(r'FirstName">', data, '<')
    MiddleName = getElement(r'MiddleName">', data, '<')
    LastName   = getElement(r'LastName">', data, '<')

    directorCSV = '%s,"%s","%s","%s"\n' % (cid, firstName, MiddleName, LastName)
    f.write(directorCSV)


def getDelimitedSections(cid, f, str, delimiter):
    remaining = len(str)
    if 0 == remaining:
        return None
    dlength = len(delimiter)
    start = str.find(delimiter)
    if (-1) == start:
        return None
    start += + dlength
    end = str.find(delimiter, start)
    processDirector(cid, f, str[start:end])
    end += dlength
    getDelimitedSections(cid, f, str[end:],delimiter)

def getCompany(xmldata, f):
    cid = getElement(r'PartyID="',xmldata,'"')
    name = getElement(r'N2:ElementType="FullName">',xmldata,'<')
    companyCSV = '%s,"%s"\n' % (cid, name)
    f.write(companyCSV)
    return cid

def getDirectors(xmldata, cid, conn):
    getDelimitedSections(cid, conn, xmldata,'N1:Director')

def readonefile(f, cfile, dfile):
    print f
    fpath = "/Users/steven/Downloads/nzbn-bulk/%s" % f
    with open(fpath, 'r') as myfile:
        xmldata = myfile.read().replace('\n', '')
        cid = getCompany(xmldata, cfile)
        getDirectors(xmldata, cid, dfile)

def readfiles():
    indir = '/Users/steven/Downloads/nzbn-bulk'
    cfile = open('nzbn_companies.csv','w')
    dfile = open('nzbn_directors.csv','w')
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            readonefile(f, cfile, dfile)

if __name__ == '__main__':
    readfiles()