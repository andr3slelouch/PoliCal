import wget
import os
def convertICStoCSV():
    print("Empezando:")
    print("Eliminando si existe")
    filename="mycalendar.ics"
    if os.path.exists(filename):
        os.remove(filename)
    url = ""
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
