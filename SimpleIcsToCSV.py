import wget
import os
import csv
import sys

def addEvent(header, filename):
    f = open(filename, "r")
    f2 = open("calendar.csv", "w+")
    f1 = f.readlines()
    print(header)
    for x in header: # Write the defenitive header
        f2.write(x)
        if x != "END":
            f2.write(";")
    f2.write("\n")
    wrBegin = False # Flag to detect the line BEGIN:VEVENT
                    # , and start saving the parameters of the event
                    # in this case is for getting the headers for the CSV
    wrNormal = False # Flag to say that is writting everything except a description
    wrDescription = False # Flag to say that is writting a description
    for x in f1: #Read all of the lines between BEGIN:VEVENT and END:VEVENT
        list = x.split(":", 1) # Separate the tags from the content, the results are limited to 2
        chars = [c for c in list[0]] # list for looking the first character on the line
        if list[0] == "BEGIN" and list[1] == "VEVENT\n": # Here an event begins
            wrNormal = True # Flag activated, for ONE EVENT
            wrBegin = True # Flag activated, for the whole set of events
            list[1] = "VEVENT" # ERASED the "\n" character
        elif list[0] == "DESCRIPTION": # Here a DESCRIPTION begins, can have a lot of lines.
            wrDescription = True # Flag activated, for the DESCRIPTION
            f2.write("\"") #  A description can be conformed by a lot of especial characters so the description will be between ""
        elif chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n' and wrDescription: # If the lines are not beginning  with an space or an "\t", means that is another tag and not currently a decription, but it can change
            wrDescription = False # Flag deactivated, it means a description content ends
            f2.write("\"" + ";") # Also finished with a semicolon
        elif list[0] == "END" and list[1] == "VEVENT\n": # An event fisnish
            wrNormal = False # Flag deactivated, a event ends
        else:
            ""

        if wrNormal and wrDescription == False: # If wrNormal is activated and wrDescription deactivated means that is every posible tag except a description
            print(list)
            try:
                removebsn = list[1].split("\n", 1) # Delete the especial character
                f2.write(removebsn[0] + ";") # Adds semicolon
            except Exception as e:
                print(e)
        elif wrNormal and wrDescription: # If wrNormal and wrDescription are activated it is a description and can have differentes kind of lines
            for y in list: #A for loop for replacing special characters as "\n", "\t" and the word "DESCRIPTION"
                new_list = {x.replace('\n', '').replace('\t', '').replace('DESCRIPTION', '')
                            for x in list}
            for x in new_list: # A for loop to add the contents to the description
                f2.write(x)
        elif wrNormal == False and wrBegin: # if wrNormal is deactivated and wrBegin activated, that means that a event has ended so a "\n" is added
            f2.write("\n")


def convertICStoCSV():
    print("Empezando:")
    print("Eliminando si existe")
    filename = "mycalendar.ics"
    if os.path.exists(filename):
        os.remove(filename)
    url = calendarurl
    wget.download(url, "mycalendar.ics")
    addEvent(findHeader(filename), filename)


def findHeader(icsCal):
    f = open(icsCal, "r")
    print("Looking for headers in this file....")
    f2 = open("calendar.csv", "w+")
    f1 = f.readlines()
    wrBegin = False # Flag to detect the line BEGIN:VEVENT
                    # , and start saving the parameters of the event
                    # in this case is for getting the headers for the CSV
    wrNormal = False
    wrDescription = False # Saving a description that could be large
    for x in f1:
        # print(x)
        # print(str(x.count('\t'))+"---"+x)
        #headers = []
        list = x.split(":", 1)
        chars = [c for c in list[0]]
        if list[0] == "BEGIN" and list[1] == "VEVENT\n": # Looking for the line that begins an event
            wrNormal = True
            wrBegin = True
        elif list[0] == "DESCRIPTION": # Looking for the line where the description begins to activate its flag
            wrDescription = True
        elif chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n' and wrDescription: # If the lines are not beginning  with an space or an "\t", means that is another tag and not currently a decription, but it can change
            wrDescription = False


        if list[0] == "END": # If the event comes to its end the flag deactivates
            wrNormal = False
        else:
            ""


        if wrNormal == False and wrBegin == True: # If all of the headers are reached it only writes and \n and stops the for loop
            f2.write("END\n")
        elif wrNormal and wrDescription == False: # Everything that can be and tag inside an event is appended to the list, but if the events are irregulars this can cause errors
            f2.write(list[0].replace(';', '') +";")
        elif wrNormal and wrDescription:
            if list[0] == "DESCRIPTION": #If the tag is description this is added, but can be lines that are part of the description
                f2.write(list[0].replace(';', '') +";")

    f2.close() # File calendar.csv is closed
    listHeaders = [] #A list of every posible header if the ics file is IRREGULAR

    with open("calendar.csv") as csv_file: # Reading the calendar.csv temporary to get the header with the most number of tags
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            listHeaders.append(row)

    filename="calendar.csv" # File name to erase the calendar.csv that is temporary
    if os.path.exists(filename):
        os.remove(filename)
    return max(listHeaders,key=len) # Get the header with the most number of tags

def main(argv):
    if len(argv) == 2: # Arguments
        filename = argv[1]
    else:
        print("python icsReader.py file/location/file.ics")
    addEvent(findHeader(filename), filename)

if __name__== "__main__":
  main(sys.argv)
