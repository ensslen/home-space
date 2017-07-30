"""
    {"decisionDateIndex_l": 20080923, "id": "ttol_08-02062-HN", "timestamp": "2011-09-22T05:32:31.173Z",
 "orderDetailCsv_s": ["\"23/09/2008\",\"47716\",\"08/02062/HN\""],
 "casePerOrg_s": ["Busch, Matthew Paul", "Mclvor, Kristen"], "tenancySuburb_s": ["ROTOTUNA"],
 "orderDetailJson_s": ["{\"dateOfIssue\":\"23/09/2008\",\"orderId\":\"47716\",\"applicationId\":\"08/02062/HN\"}"],
 "tenancyStreetName_s": ["FENDALTON"], "casePerOrgLastName_s": ["Busch", "Mclvor"],
 "applicationNumber_s": ["08/02062/HN"], "casePerOrgApplicant_s": ["Busch, Matthew Paul"],
 "applicationId_s": ["08/02062/HN"], "casePerOrgFirstName_s": ["Kristen", "Matthew"],
 "publishedDate_s": ["2008-09-23 00:00:00.0"], "tenancyStreetNumber_s": ["10"],
 "casePerOrgRespondent_s": ["Mclvor, Kristen"], "jurisdictionCode_s": ["TT"],
 "jurisdictionName_s": ["Tenancy Tribunal"], "casePerOrgFirstName_txt": ["Kristen", "Matthew"], "orderDetailXml_s": [
    "<orderDetail><dateOfIssue>23/09/2008</dateOfIssue><orderId>47716</orderId><applicationId>08/02062/HN</applicationId></orderDetail>"],
 "tenancyStreetType_s": ["DRIVE"], "tenancyCityTown_s": ["HAMILTON"],
 "tenancyAddress_txt": ["10 FENDALTON DRIVE ,ROTOTUNA, HAMILTON"],
 "tenancyAddress_s": ["10 FENDALTON DRIVE ,ROTOTUNA, HAMILTON"], "casePerOrgLastName_txt": ["Busch", "Mclvor"]}
"""

import os
import json

def myGet(d, selector):
    if selector in d:
        return json.dumps(d[selector]).replace('"', '')
    else:
        return ''

def handleDecision(d):
    return '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (
        myGet(d, 'id'),
        myGet(d, 'applicationId_s'),
        myGet(d, 'applicationNumber_s'),
        myGet(d, 'casePerOrg_s'),
        myGet(d, 'casePerOrgApplicant_s'),
        myGet(d, 'casePerOrgFirstName_s'),
        myGet(d, 'casePerOrgLastName_txt'),
        myGet(d, 'casePerOrgOrganisationName_s'),
        myGet(d, 'casePerOrgRespondent_s'),
        myGet(d, 'decisionDateIndex_l'),
        myGet(d, 'jurisdictionName_s'),
        myGet(d, 'jurisdictionCode_s'),
        myGet(d, 'orderDetailCsv_s'),
        myGet(d, 'orderDetailJson_s'),
        myGet(d, 'orderDetailXml_s'),
        myGet(d, 'publishedDate_s'),
        myGet(d, 'tenancyAddress_txt'),
        myGet(d, 'tenancyCityTown_s'),
        myGet(d, 'tenancyStreetName_s'),
        myGet(d, 'tenancyStreetNumber_s'),
        myGet(d, 'tenancyStreetType_s'),
        myGet(d, 'tenancySuburb_s'))


def handleDecisions(arr, f):
    for d in arr:
        f.write(handleDecision(d))

def readonefile(inF, outF):
    print inF
    textData = open(inF,'r')
    data = json.load(textData)
    handleDecisions(data['response']['docs'], outF)


def readfiles():
    indir = '/Users/steven/Downloads/tt'
    tfile = open('tenancy.csv','w')
    #dfile = open('nzbn_directors.csv','w')
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            if f.endswith(".json"):
                readonefile('%s/%s' %(indir,f), tfile )

if __name__ == '__main__':
    #readonefile('/Users/steven/Downloads/tt/decisions-200809.json')
    readfiles()