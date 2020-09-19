"""
.. module:: SimpleIcsToCSV
   :platform: Unix, Windows
   :synopsis: This module converts ICS calendar file from moodle to CSV file.

.. moduleauthor:: Luis Andrade <andr3slelouch@github.com>


"""
import wget
import os
import csv
import sys
from polical import configuration

import logging

EXPORT_FILENAME = "calendar.csv"
VEVENT_WITH_LINE_BREAK = "VEVENT\n"

logging.basicConfig(
    filename=configuration.get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def add_event(header: list, filename: str):
    """This function adds a event as a new line in csv file.

    Args:
        header (list): Header for the csv.
        filename (str): The filename where file would be written.

    Returns:
        None. If not has headers
    """
    if not header:
        return None
    f = open(configuration.get_file_location(filename), "r", encoding="utf-8")
    f2 = open(configuration.get_file_location(EXPORT_FILENAME), "w+")
    f1 = f.readlines()
    # print(header)
    for x in header:  # Write the defenitive header
        f2.write(x)
        if x != "END":
            f2.write(";")
    f2.write("\n")
    begin_writing_bool = False  # Flag to detect the line BEGIN:VEVENT
    # , and start saving the parameters of the event
    # in this case is for getting the headers for the CSV
    normal_writing_bool = (
        False  # Flag to say that is writting everything but no description
    )
    description_writing_bool = False  # Flag to say that is writting a description
    for x in f1:  # Read all of the lines between BEGIN:VEVENT and END:VEVENT
        # Separate the tags from the content, the results are limited to 2
        line_list = x.split(":", 1)
        # list for looking the first character on the line
        chars = [c for c in line_list[0]]
        if (
            line_list[0] == "BEGIN" and line_list[1] == VEVENT_WITH_LINE_BREAK
        ):  # Here an event begins
            normal_writing_bool = True  # Flag activated, for ONE EVENT
            begin_writing_bool = True  # Flag activated, for the whole set of events
            line_list[1] = "VEVENT"  # ERASED the "\n" character
        # Here a DESCRIPTION begins, can have a lot of lines.
        elif line_list[0] == "DESCRIPTION":
            description_writing_bool = True  # Flag activated, for the DESCRIPTION
            # A description can be conformed by a lot of especial characters so
            # the description will be between ""
            f2.write('"')
        # If the lines are not beginning  with an space or an "\t", means that
        # is another tag and not currently a decription, but it can change
        elif (
            chars[0] != " "
            and chars[0] != "\t"
            and chars[0] != "\n"
            and description_writing_bool
        ):
            description_writing_bool = (
                False  # Flag deactivated, it means a description content ends
            )
            f2.write('"' + ";")  # Also finished with a semicolon
        elif (
            line_list[0] == "END" and line_list[1] == VEVENT_WITH_LINE_BREAK
        ):  # An event fisnish
            normal_writing_bool = False  # Flag deactivated, a event ends

        if normal_writing_bool and description_writing_bool == False:
            # If normal_writing_bool is activated and description_writing_bool deactivated means that
            # is every posible tag except a description
            # print(list)
            try:
                # Delete the especial character
                removebsn = line_list[1].split("\n", 1)
                f2.write(removebsn[0].replace(";", "") + ";")
                # Adds semicolon and avoids double ";"
            except Exception as e:
                print(e)
        elif normal_writing_bool and description_writing_bool:
            # If normal_writing_bool and description_writing_bool are
            # activated it is a description and can have differentes kind of
            # lines

            new_list = {
                x.replace("\n", "").replace("\t", "").replace("DESCRIPTION", "")
                for x in line_list
            }
            for x in new_list:  # A for loop to add the contents to the description
                f2.write(x)
        elif normal_writing_bool == False and begin_writing_bool:
            # if normal_writing_bool is deactivated and begin_writing_bool activated, that means that
            # a event has ended so a "\n" is added
            f2.write("\n")


def convert_ics_to_csv(url: str):
    """This function downloads the moodle calendar and addEvents to a CSV file.

    Args:
        url (str): URL to download moodle calendar
    """
    print("Descargando calendario desde Aula Virtual...")
    logging.info("Descargando calendario desde Aula Virtual...")
    filename = configuration.get_file_location("mycalendar.ics")
    if os.path.exists(filename):
        os.remove(filename)
    wget.download(url, filename)
    add_event(find_header(filename), filename)
    print("\nEspere...")
    logging.info("Descarga de calendario finalizada.")


def find_header(filename: str) -> list:
    """This function looks for all the file to get the most longest header.

    Args:
        icsCal (str): The ics file location.

    Returns:
        (list): List containing the largest header list.
    """
    f = open(configuration.get_file_location(filename), "r", encoding="utf-8")
    f2 = open(configuration.get_file_location(EXPORT_FILENAME), "w+")
    f1 = f.readlines()
    begin_writing_bool = False  # Flag to detect the line BEGIN:VEVENT
    # , and start saving the parameters of the event
    # in this case is for getting the headers for the CSV
    normal_writing_bool = False
    description_writing_bool = False  # Saving a description that could be large
    for x in f1:
        line_list = x.split(":", 1)
        chars = [c for c in line_list[0]]
        # Looking for the line that begins an event
        if line_list[0] == "BEGIN" and line_list[1] == VEVENT_WITH_LINE_BREAK:
            normal_writing_bool = True
            begin_writing_bool = True
        # Looking for the line where the description begins to activate its
        # flag
        elif line_list[0] == "DESCRIPTION":
            description_writing_bool = True
        # If the lines are not beginning  with an space or an "\t", means that
        # is another tag and not currently a decription, but it can change
        elif (
            chars[0] != " "
            and chars[0] != "\t"
            and chars[0] != "\n"
            and description_writing_bool
        ):
            description_writing_bool = False

        if line_list[0] == "END":  # If the event comes to its end the flag
            # deactivates
            normal_writing_bool = False
        else:
            ""

        # If all of the headers are reached it only writes and \n and stops the for loop
        if normal_writing_bool == False and begin_writing_bool == True:
            f2.write("END\n")
        elif normal_writing_bool and description_writing_bool == False:
            # Everything that can be and tag inside an event is appended to the
            # list, but if the events are irregulars this can cause errors
            f2.write(line_list[0].replace(";", "") + ";")
        elif (
            normal_writing_bool
            and description_writing_bool
            and line_list[0] == "DESCRIPTION"
        ):
            # If the tag is description this is added, but can be lines that
            # are part of the description
            f2.write(line_list[0].replace(";", "") + ";")

    f2.close()  # File calendar.csv is closed
    headers_list = []  # A list of every posible header if the ics file is
    # IRREGULAR

    # Reading the calendar.csv temporary to get the header with the most number
    # of tags
    with open(configuration.get_file_location(EXPORT_FILENAME)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            headers_list.append(row)

    # File name to erase the calendar.csv that is temporary
    filename = configuration.get_file_location(EXPORT_FILENAME)
    if os.path.exists(filename):
        os.remove(filename)
    # Get the header with the most number of tags
    if len(headers_list) > 1:
        return max(headers_list, key=len)
    else:
        return []


def main(argv):
    if len(argv) == 2:  # Arguments
        filename = argv[1]
        add_event(find_header(filename), filename)
    else:
        print("python SimpleIcsToCSV.py file/location/file.ics")
        logging.info("python SimpleIcsToCSV.py file/location/file.ics")


if __name__ == "__main__":
    main(sys.argv)
