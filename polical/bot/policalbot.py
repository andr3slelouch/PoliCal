import os
import sys
import html
import telegram
import yaml
from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)
from telegram.ext.dispatcher import run_async
from polical import configuration
from polical import connectSQLite
from polical import tasks_processor
from polical import MateriaClass, TareaClass
import re
import json
import logging
import traceback
import pytz
from datetime import datetime, timezone, timedelta

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
CALENDAR_MOODLE_EPN_URL = "https://aulasvirtuales.epn.edu.ec/calendar/export.php?"
CREATED_REMINDERS_OLD_TASKS = True
START_BOT_DATETIME = datetime.now(timezone.utc)


def start(update: Update, context: CallbackContext) -> None:
    """This command handler starts the bot interactions it sends a message to the user with the instructions to use the bot"""

    username = update.message.from_user["id"]
    message = (
        "Bienvenido a PoliCal!\n"
        + "Recuerde que antes de iniciar el proceso de obtención de credenciales ud debe tener una cuenta en el Aula Virtual, y deben estar iniciadas las sesiones en el navegador predeterminado"
        + f"\nAcceda al siguiente enlace: {CALENDAR_MOODLE_EPN_URL} "
        + "\nA continuación se abrirá un link hacia el Aula Virtual EPN: \n 1. En proximos eventos para: elija Todos los cursos"
        + "\n 2. A continuación desplácese a la parte más inferior de la página y de clic en el botón Exportar Calendario"
        + '\n 3. Luego, en la opción Exportar seleccione todos los eventos\n 4. Después en "para" seleccione los 60 días recientes y próximos'
        + "\n 5. Finalmente de clic en el boton Obtener URL del calendario"
        + "\n 6. Responda con /url y el enlace obtenido"
    )
    if not connectSQLite.check_user_existence(username):
        connectSQLite.save_user(username)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
    )


def get_moodle_epn_url(update: Update, context: CallbackContext) -> None:
    """This command handler is made for receiving the moodle url from the user and saves it to the database"""

    username = update.message.from_user["id"]
    try:
        calendar_url = " ".join(context.args).replace("\n", "")
        if configuration.check_for_url(calendar_url):
            connectSQLite.save_user_calendar_url(calendar_url, username)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Utilice /update para obtener sus tareas",
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Algo salió mal mientras se registraba la url,"
                + " verifique y reintente",
            )
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Algo salió mal mientras se registraba la url,"
            + " verifique y reintente",
        )


def save_subject_command(update: Update, context: CallbackContext) -> None:
    """This command handler saves a subject if is not registerd in the database"""

    username = update.message.from_user["id"]
    new_subject = " ".join(context.args)

    try:
        subject_code = re.search("\(([^)]+)", new_subject).group(1)

        subject_new_name = MateriaClass.Materia(new_subject, subject_code)
        connectSQLite.save_user_subject_name(subject_new_name, username)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Materia " + new_subject + " registrada",
        )
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Algo salió mal mientras se registraba la materia,"
            + " recuerde incluir el código de la materia dentro de parentesis",
        )


def callback_reminder_message(context: CallbackContext) -> None:
    """This callback handler registers a new job for remind the user about a task 30 minutes before due the task"""

    (chat_id, text_message, message_id) = context.job.context
    logger.info(
        "Added new reminder for task: "
        + str(text_message)
        + " for user: "
        + str(chat_id)
    )
    try:
        context.bot.send_message(
            chat_id=chat_id, text=text_message, reply_to_message_id=message_id
        )
    except Exception as e:
        logger.warning("cannot reply message {}: {}".format(message_id, e))


def get_new_tasks(context: CallbackContext) -> None:
    """This functions repeats in specific times, looks for new tasks for every user that has a valid url registered in the database,
    also defines new jobs for reminder incoming tasks for the users"""

    users_with_url = connectSQLite.get_all_users_with_URL()
    task_bot_datetime = datetime.now(timezone.utc)
    logger.info("get_new_tasks started")
    print("get_new_tasks started")
    for user_with_url in users_with_url:
        username = user_with_url["username"]
        calendar_url = user_with_url["url"]
        tasks_processor.save_tasks_to_db(calendar_url, username, {}, False)
        tasks = connectSQLite.get_tasks_for_bot(username, task_bot_datetime)
        sended_tasks = connectSQLite.get_sended_tasks_for_bot(
            username, START_BOT_DATETIME
        )
        global CREATED_REMINDERS_OLD_TASKS
        if len(sended_tasks) > 0 and CREATED_REMINDERS_OLD_TASKS:
            for sended_task in sended_tasks:
                context.job_queue.run_once(
                    callback_reminder_message,
                    sended_task["due"],
                    context=(
                        username,
                        "La tarea " + str(sended_task["title"]) + " expirará pronto",
                        sended_task["tid"],
                    ),
                )
        if len(tasks) > 0:
            send_new_tasks(context, username, tasks)
        CREATED_REMINDERS_OLD_TASKS = False


def send_new_tasks(context: CallbackContext, username: str, tasks: list) -> None:
    """This function sends the tasks as messages to the users also registers josb for new task and remidner to the user

    Args:
        context (CallbackContext): Context sended by the main command handler
        username (str): username to send the message
        tasks (list): List of tasks to be sended to the user
    """
    for task in tasks:
        message = task.summary()
        sended_msg = None
        try:
            sended_msg = context.bot.send_message(
                chat_id=username,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
            )
        except:
            sended_msg = context.bot.send_message(chat_id=username, text=message)
        task.define_tid(sended_msg.message_id)
    for task in tasks:
        if task.tid:
            connectSQLite.add_task_tid(str(task.id), str(task.tid), str(username))
            context.job_queue.run_once(
                callback_reminder_message,
                task.due_date - timedelta(minutes=30),
                context=(
                    username,
                    "La tarea " + task.title + " expirará pronto",
                    task.tid,
                ),
            )


def get_jobs(update: Update, context: CallbackContext) -> None:
    """This function is made to kno how much jobs are currently executing"""
    username = update.message.from_user["id"]
    if username == 232424901:
        context.bot.send_message(
            chat_id=232424901,
            text="Number of jobs " + str(len(context.job_queue.jobs())),
        )


def get_tasks(update: Update, context: CallbackContext) -> None:
    """This command handler is made for updating and sending the tasks to the users"""
    username = update.message.from_user["id"]
    calendar_url = connectSQLite.get_user_calendar_url(username)
    tasks_processor.save_tasks_to_db(calendar_url, username, {}, False)
    tasks = connectSQLite.get_tasks_for_bot(username, update.message.date)
    sended_tasks = connectSQLite.get_sended_tasks_for_bot(username, update.message.date)
    if len(tasks) == 0 and len(sended_tasks) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No existen tareas nuevas, verifique consultando el calendario",
        )
    else:
        for task in sended_tasks:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=task["title"],
                reply_to_message_id=int(task["tid"]),
            )
        send_new_tasks(context, username, tasks)


def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    context.bot.send_message(chat_id=232424901, text=message, parse_mode=ParseMode.HTML)


def run():
    configuration.set_preffered_dbms("mysql")
    print("BOT STARTED...")
    updater = Updater(
        token=configuration.get_bot_token(
            configuration.get_file_location("config.yaml")
        ),
        use_context=True,
    )

    dispatcher = updater.dispatcher

    job_queue_manager = updater.job_queue

    start_handler = CommandHandler("start", start)
    moodle_epn_handler = CommandHandler("url", get_moodle_epn_url)
    get_tasks_handler = CommandHandler("update", get_tasks)
    save_subject_handler = CommandHandler("subject", save_subject_command)
    get_jobs_handler = CommandHandler("jobs", get_jobs)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(moodle_epn_handler)
    dispatcher.add_handler(get_tasks_handler)
    dispatcher.add_handler(save_subject_handler)
    dispatcher.add_handler(get_jobs_handler)

    job_queue_manager.run_repeating(get_new_tasks, interval=60 * 60 * 1, first=10)

    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
