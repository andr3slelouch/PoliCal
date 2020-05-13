import wget
import os
from polical import configuration
import logging
logging.basicConfig(filename=configuration.get_file_location('Running.log'),level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def convertICStoCSV():
    logging.info("Empezando:")
    logging.infoc("Eliminando si existe")
    print("Empezando:")
    print("Eliminando si existe")
    filename="mycalendar.ics"
    if os.path.exists(filename):
        os.remove(filename)
    url = "https://educacionvirtual.epn.edu.ec/calendar/export_execute.php?userid=7587&authtoken=a43c2f67460752ab1e1b0d5a784dd330cb5b93e7&preset_what=all&preset_time=recentupcoming"
    wget.download(url, "mycalendar.ics")
    f = open("mycalendar.ics","r")
    f2 = open("calendar.csv","w+")
    f1 = f.readlines()
    headers = ["BEGIN","UID","SUMMARY","DESCRIPTION","CLASS","LAST-MODIFIED","DTSTAMP","DTSTART","DTEND","CATEGORIES"]
    for x in headers:
        f2.write(x+";")
    f2.write("\n")
    wrBegin=False
    wrNormal=False
    wrDescription=False
    for x in f1:
        #print(x)
        #print(str(x.count('\t'))+"---"+x)
        list = x.split(":",1)
        if list[0]=="BEGIN" and list[1]=="VEVENT\n":
            wrNormal=True
            wrBegin=True
            list[1]="VEVENT"
            #print(list[1])
        elif list[0]=="DESCRIPTION":
            wrDescription=True
            f2.write("\"")
            #print(list[0])
        elif list[0]=="CLASS":
            wrDescription=False
            f2.write("\""+";")
            #print(list[0])
        elif list[0]=="END" and list[1]=="VEVENT\n":
            wrNormal=False
            #print(list[0])
        else:
            ""
        if wrNormal and wrDescription==False:
            removebsn=list[1].split("\n",1)
            f2.write(removebsn[0]+";")
        elif wrNormal and wrDescription:
            for y in list:
                new_list = {x.replace('\n', '').replace('\t', '') for x in list}
                for x in new_list:
                    f2.write(x)
        elif wrNormal==False and wrBegin:
            f2.write("\n")
