import urllib2
import urlparse
import zipfile
import StringIO
from datetime import datetime
import time
from time import gmtime, strftime
from pandas import *
import os

HDR = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
      }


def dategenerator():
    # 19 -8-2010 to 19-8-2012
    # 20-8-2012 to 19-8-2015
    start = datetime(2012, 8, 20)
    end = datetime(2015, 8, 19)
    rng = bdate_range(start, end).date
    for i in rng:
        getreq(i.strftime('%d-%b-%Y'))


def getreq(date):

    splitList = date.split('-')
    month = date.split('-')[1].upper()
    year = date.split('-')[2]
    fileName = "".join([splitList[0], month, year])
    # SITE = "http://www.nseindia.com/content/historical/EQUITIES/2015/AUG/
    # cm14AUG2015bhav.csv.zip"
    SITE = "http://www.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}bhav.csv.zip".format(year, month, fileName)
    req = urllib2.Request(SITE, headers=HDR)
    getfile(req)


def getfile(pageReq):
    try:
        page = urllib2.urlopen(pageReq)
        z = zipfile.ZipFile(StringIO.StringIO(page.read()))
        z.extractall()
        print "Success"
    except urllib2.HTTPError, e:
        print "Failed"
        return


def fileRename():
    os.chdir("/scripts/Data/")
    for files in os.listdir("/scripts/Data/"):
        newFileName = files[2:4]+"-"+files[4:7]+"-"+files[7:11]+".csv"
        os.rename(files, newFileName)
        print "Success"


def fileYearWrite(year):
    DIRPATH = "/scripts/Data/"
    fout = open("%d.csv" %year, "wb")
    headerCount = 0
    # os.chdir(DIRPATH)
    for files in os.listdir(DIRPATH):
        yearFromFile = files.split("-")[2].split(".")[0]
        if int(yearFromFile) == year:
            print yearFromFile
            fileIn = open(DIRPATH+files)
            if headerCount == 0:
                for line in fileIn:
                    fout.write(line)
                headerCount += 1
            else:
                fileIn.next()
                for line in fileIn:
                    fout.write(line)
        else:
            continue
        fileIn.close()
    fout.close()


def yearlySplit():
    years = [2010, 2011, 2012, 2013, 2014, 2015]
    for element in years:
        fileYearWrite(element)


def fileWeeklyWrite(dates):
    DIRPATH = "scripts/temp/"
    # making a reference date and week number
    refYear = dates.split("-")[2].split(".")[0]
    refDate = dates.split(".")[0]
    t = time.strptime(refDate, "%d-%b-%Y")
    refWeekNumber = strftime("%U", t)
    fout = open("{}-{}.csv".format(refYear,refWeekNumber),"wb")
    headerCount = 0
    # traversing through all the files in the dir
    for files in os.listdir(DIRPATH):
        yearFromFile = files.split("-")[2].split(".")[0]
        dateFromFile = files.split(".")[0]
        d = time.strptime(dateFromFile, "%d-%b-%Y")
        weekNumber = strftime("%U", d)
        if int(yearFromFile) == int(refYear) and int(weekNumber) == int(refWeekNumber):
            fileIn = open(DIRPATH+files)
            if headerCount == 0:
                for line in fileIn:
                    fout.write(line)
                headerCount += 1
            else:
                fileIn.next()
                for line in fileIn:
                    fout.write(line)
        else:
            continue
        fileIn.close()
    fout.close()


def weeklySplit():
    DIRPATH = "/scripts/temp/"
    for files in os.listdir(DIRPATH):
        dateFromFile = files.split(".")[0]
        print dateFromFile
        fileWeeklyWrite(dateFromFile)
# dategenerator()
# fileRename()
# yearlySplit()
weeklySplit()
