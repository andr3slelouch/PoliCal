from trello import TrelloClient
from pathlib import Path
from polical import configuration
import os
import yaml
import logging


def get_trello_client(user_dict: dict) -> TrelloClient:
    """This function gets a Trello Client Object to connect to Trello.

    Args:
        user_dict (dict): File path for the config file to be loaded

    Returns:
        client (TrelloClient): Client object that has access to Trello.
    """
    client = TrelloClient(
        api_key=user_dict["api_key"],
        api_secret=user_dict["api_secret"],
        token=user_dict["oauth_token"],
        token_secret=user_dict["oauth_token_secret"],
    )

    return client


def get_uncompleted_cards() -> list:
    """This function gets a all uncompleted cards from a board.

    Returns:
        uncompleted_cards (List): List of strings from all uncompleted cards
    """
    user = configuration.load_config_file("trelloCredentials.yaml")
    client = get_trello_client(user)
    all_boards = client.list_boards()
    # last_board = all_boards[-1]
    uncompleted_cards = []
    for last_board in all_boards:
        if last_board.name == "TareasPoli":
            for list_from_board in last_board.list_lists():
                for card in list_from_board.list_cards():
                    if card.due is not None and not card.is_due_complete:
                        uncompleted_cards.append(
                            card.name + " | " + list_from_board.name + "\n"
                        )
    return uncompleted_cards


def get_cards_urls() -> list:
    """This function gets a all uncompleted cards from a board.

    Returns:
        uncompleted_cards (List): List of strings from all uncompleted cards
    """
    user = configuration.load_config_file("trelloCredentials.yaml")
    client = get_trello_client(user)
    all_boards = client.list_boards()
    last_board = all_boards[-1]
    uncompleted_cards = []
    last_list_from_board = last_board.list_lists()[-1]
    for card in last_list_from_board.list_cards():
        uncompleted_cards.append(
            card.name + " | " + last_list_from_board.name + " | " + card.url + "\n"
        )
    return uncompleted_cards


def get_todo_tasks() -> list:
    """This function gets a all tasks that exits on todo.txt.

    Returns:
        tasks_list (List): List of strings from all tasks that exits on todo.txt
    """
    with open(configuration.get_file_location("todo.txt"), "r") as todo:
        tasks_list = todo.readlines()
        return tasks_list


def write_todo_tasks(tasks_list: list):
    """This function writes all tasks from a list.

    Args:
        tasks_list (list): List containing tasks to be added to the todo.txt file
    """
    with open(configuration.get_file_location("todo.txt"), "w") as todo:
        todo.writelines(tasks_list)


def update_new_taks():
    """This function collects all new tasks from trello and concatenates to existing todo.txt file"""
    current_tasks = []
    current_tasks = get_todo_tasks()
    uncompleted_tasks = []
    uncompleted_tasks = get_uncompleted_cards()
    for task in current_tasks:
        if task in uncompleted_tasks:
            uncompleted_tasks.remove(task)
    if uncompleted_tasks:
        current_tasks += uncompleted_tasks
        write_todo_tasks(current_tasks)
    else:
        print("No existen nuevas tareas para añadir a todo.txt")


def get_done_tasks() -> list:
    """This function gets a all tasks that exits on todo.txt.

    Returns:
        tasks_list (List): List of strings from all tasks that exits on todo.txt
    """
    with open(configuration.get_file_location("done.txt"), "r") as done:
        readed_lines = done.readlines()
        done_list = []
        for done_item in readed_lines:
            done_list.append(done_item.split(" ", 2))
        return done_list


def update_done_taks():
    """This functions gets new done tasks and updates to the cards on trello"""
    done_tasks_to_trello = []
    for done in get_done_tasks():
        splitted = done[2].split("|")
        if len(splitted) == 2:
            splitted[0] = splitted[0].rstrip()
            splitted[1] = splitted[1].strip().replace("\n", "")
            done_tasks_to_trello.append(splitted)

    user = configuration.load_config_file("trelloCredentials.yaml")
    client = get_trello_client(user)
    all_boards = client.list_boards()
    # last_board = all_boards[-1]  # Error cuando se cree un nuevo board
    for last_board in all_boards:
        if last_board.name == "TareasPoli":
            for done_task in done_tasks_to_trello:
                for list_from_board in last_board.list_lists():
                    if list_from_board.name == done_task[1]:
                        for card in list_from_board.list_cards():
                            if card.name == done_task[0] and not card.is_due_complete:
                                card.set_due_complete()
                                print("Updated", card.name, "to DONE")


def generate_todo_txt():
    print("Actualizando trello desde done.txt...")
    update_done_taks()
    print("Generando nuevas tareas para todo.txt...")
    update_new_taks()