import os
import webbrowser
import getpass

darPermisos= 'https://myaccount.google.com/lesssecureapps'
print('   ')
print("====================")
print('Para activar este servicio es indispensable disponer de una cuenta de correo en Gmail, además es necesario permitir el acceso de apps menos seguras, para esto puedes dirigirte al siguiente enlace y dar lo permisos necesarios:')
print('   '+ darPermisos)
input("Presione ENTER para ir al enlace y dar permisos")
webbrowser.open_new_tab(darPermisos)

correoEnvio= input("Introduce tu correo de gmail el cual va a realizar las notificaciones: "+ os.linesep)
clave= getpass.getpass("Ingresa la contraseña del correo: ")
correoNotifica= input("Introduce el correo al cual van a llegar las notificaciones: "+ os.linesep)


file =open("EnvioMail.py", "w")

file.write("import smtplib"+ os.linesep+ "import getpass"+ os.linesep)

file.write("message= 'Tiene un nueva tarea por favor revise su aula virtual'"+ os.linesep+ "subject = 'Nueva tarea Aula virtual'"+ os.linesep+ os.linesep)

file.write("message = 'Subject: {}\\"+ "n\\"+ "n{}'.format(subject, message)"+ os.linesep)





file.write("server= smtplib.SMTP('smtp.gmail.com', 587)"+ os.linesep + "server.starttls()"+ os.linesep+ os.linesep)

file.write("server.login('"+correoEnvio + "', '"+ clave+ "')"+ os.linesep)
file.write("server.sendmail('"+correoEnvio+ "', '"+ correoNotifica+"', "+ "message)"+ os.linesep)
file.write("server.quit()"+ os.linesep)
file.close()

print('Cuenta configurada exitosamente')










