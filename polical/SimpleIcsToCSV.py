import wget
import os
import csv
import sys
from polical import configuration

import logging
logging.basicConfig(filename=configuration.get_file_location('Running.log'),level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def addEvent(header, filename):
    f = open(configuration.get_file_location(filename), "r", encoding='utf-8')
    f2 = open(configuration.get_file_location("calendar.csv"), "w+")
    f1 = f.readlines()
    # print(header)
    for x in header:  # Write the defenitive header
        f2.write(x)
        if x != "END":
            f2.write(";")
    f2.write("\n")
    wrBegin = False  # Flag to detect the line BEGIN:VEVENT
    # , and start saving the parameters of the event
    # in this case is for getting the headers for the CSV
    wrNormal = False  # Flag to say that is writting everything but no description
    wrDescription = False  # Flag to say that is writting a description
    for x in f1:  # Read all of the lines between BEGIN:VEVENT and END:VEVENT
        # Separate the tags from the content, the results are limited to 2
        list = x.split(":", 1)
        # list for looking the first character on the line
        chars = [c for c in list[0]]
        if list[0] == "BEGIN" and list[1] == "VEVENT\n":  # Here an event begins
            wrNormal = True  # Flag activated, for ONE EVENT
            wrBegin = True  # Flag activated, for the whole set of events
            list[1] = "VEVENT"  # ERASED the "\n" character
        # Here a DESCRIPTION begins, can have a lot of lines.
        elif list[0] == "DESCRIPTION":
            wrDescription = True  # Flag activated, for the DESCRIPTION
            # A description can be conformed by a lot of especial characters so
            # the description will be between ""
            f2.write("\"")
        # If the lines are not beginning  with an space or an "\t", means that
        # is another tag and not currently a decription, but it can change
        elif chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n' and wrDescription:
            wrDescription = False  # Flag deactivated, it means a description content ends
            f2.write("\"" + ";")  # Also finished with a semicolon
        elif list[0] == "END" and list[1] == "VEVENT\n":  # An event fisnish
            wrNormal = False  # Flag deactivated, a event ends
        else:
            ""

        if wrNormal and wrDescription == False:
            # If wrNormal is activated and wrDescription deactivated means that
            # is every posible tag except a description
            # print(list)
            try:
                # Delete the especial character
                removebsn = list[1].split("\n", 1)
                f2.write(removebsn[0] + ";")  # Adds semicolon
            except Exception as e:
                print(e)
        elif wrNormal and wrDescription:  # If wrNormal and wrDescription are
            # activated it is a description and can have differentes kind of
            # lines
            for y in list:  # A for loop for replacing special characters as
                # "\n", "\t" and the word "DESCRIPTION"
                new_list = {x.replace('\n', '').replace('\t', '').replace('DESCRIPTION', '')
                            for x in list}
            for x in new_list:  # A for loop to add the contents to the description
                f2.write(x)
        elif wrNormal == False and wrBegin:
            # if wrNormal is deactivated and wrBegin activated, that means that
            # a event has ended so a "\n" is added
            f2.write("\n")


def convertICStoCSV(url):
    # print("Empezando:")
    # print("Eliminando si existe")
    print("Descargando calendario desde Aula Virtual...")
    logging.info("Descargando calendario desde Aula Virtual...")
    filename = configuration.get_file_location("mycalendar.ics")
    if os.path.exists(filename):
        os.remove(filename)
    # aurl = configuration.load_config_file('polical.yaml')['calendar_url']
    wget.download(url, filename)
    addEvent(findHeader(filename), filename)
    print("\nEspere...")
    logging.info("Descarga de calendario finalizada.")

def findHeader(icsCal):
    f = open(configuration.get_file_location(icsCal), "r", encoding="utf-8")
    # print("Looking for headers in this file....")
    f2 = open(configuration.get_file_location("calendar.csv"), "w+")
    f1 = f.readlines()
    wrBegin = False  # Flag to detect the line BEGIN:VEVENT
    # , and start saving the parameters of the event
    # in this case is for getting the headers for the CSV
    wrNormal = False
    wrDescription = False  # Saving a description that could be large
    for x in f1:
        # print(x)
        # print(str(x.count('\t'))+"---"+x)
        # headers = []
        list = x.split(":", 1)
        chars = [c for c in list[0]]
        # Looking for the line that begins an event
        if list[0] == "BEGIN" and list[1] == "VEVENT\n":
            wrNormal = True
            wrBegin = True
        # Looking for the line where the description begins to activate its
        # flag
        elif list[0] == "DESCRIPTION":
            wrDescription = True
        # If the lines are not beginning  with an space or an "\t", means that
        # is another tag and not currently a decription, but it can change
        elif chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n' and wrDescription:
            wrDescription = False

        if list[0] == "END":  # If the event comes to its end the flag
            # deactivates
            wrNormal = False
        else:
            ""

        # If all of the headers are reached it only writes and \n and stops the for loop
        if wrNormal == False and wrBegin == True:
            f2.write("END\n")
        elif wrNormal and wrDescription == False:
            # Everything that can be and tag inside an event is appended to the
            # list, but if the events are irregulars this can cause errors
            f2.write(list[0].replace(';', '') + ";")
        elif wrNormal and wrDescription:
            # If the tag is description this is added, but can be lines that
            # are part of the description
            if list[0] == "DESCRIPTION":
                f2.write(list[0].replace(';', '') + ";")

    f2.close()  # File calendar.csv is closed
    listHeaders = []  # A list of every posible header if the ics file is
    # IRREGULAR

    # Reading the calendar.csv temporary to get the header with the most number
    # of tags
    with open(configuration.get_file_location("calendar.csv")) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # line_count = 0
        for row in csv_reader:
            listHeaders.append(row)

    # File name to erase the calendar.csv that is temporary
    filename = configuration.get_file_location("calendar.csv")
    if os.path.exists(filename):
        os.remove(filename)
    # Get the header with the most number of tags
    return max(listHeaders, key=len)


def main(argv):
    if len(argv) == 2:  # Arguments
        filename = argv[1]
    else:
        print("python icsReader.py file/location/file.ics")
        logging.info("python icsReader.py file/location/file.ics")
    addEvent(findHeader(filename), filename)


if __name__ == "__main__":
    main(sys.argv)
