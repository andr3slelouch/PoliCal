import TareasCSVToBD
import SendTaskToTrello
import SimpleIcsToCSV
SimpleIcsToCSV.convertICStoCSV()
TareasCSVToBD.LoadCSVTasktoDB()
SendTaskToTrello.SendTaskToTrello()
