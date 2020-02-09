import TareasCSVToBD
import SendTaskToTrello
import SimpleIcsToCSV
import ConfigurarEmail

SimpleIcsToCSV.convertICStoCSV()
TareasCSVToBD.LoadCSVTasktoDB()
SendTaskToTrello.SendTaskToTrello()


