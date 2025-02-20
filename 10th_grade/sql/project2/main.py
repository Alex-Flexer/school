"""Module provides beautiful printing tables"""
import os
import difflib
import logging

from sqlalchemy.orm.session import Session as SessionType
from tabulate import tabulate

from db import Session
from db.models import Task, Profile, Project, User


# cache = {}
# COMMANDS = [
#     "all", "a", "all-free", "af", "quit",
#     "find-user", "fu", "search", "find", "exit",
#     "s", "f", "my", "help", "h", "sign-in", "q",
#     "si", "sign-up", "su", "delete", "del", "d",
#     "delete-user", "del-user", "du", "borrow",
#     "br", "take-back", "tb", "relocate", "rl",
#     "move", "mv", "add", "create", "cr", "remove", "rm"
# ]


def welcome():
    """
    Function print welcome
    """
    print("Welcome to Flexer-Lib-System!\n"
          "To get instruction use \"help\" (h)\n\n")


def pprint(*args, **kwargs):
    """
    Function provides printing with clearing
    """
    os.system("cls")
    print(*args, **kwargs)


def get_acceptation(text: str) -> bool:
    """
    Function checks acceptation from user
    """
    acceptation = input(f"{text} [Y]es|[N]o: ")
    if acceptation.lower() not in ("yes", "y", ""):
        print("Operation was successfully canceled.")
        return False
    return True


def main():
    """
    Just main
    """
    session: SessionType = Session()

    # welcome()

    while user_input := input(">>> "):
        pprint(end="")
        cmd = user_input
        match cmd:
            case "add-user" | "au":
                username = input("User's username: ")
                email = input("User's email: ")
                if session.query(User).filter_by(username=username, email=email).count() > 0:
                    print("User with this username of with this email already exists.")
                else:
                    bio = input("Profile's biography: ")
                    phone = input("Profile's phone number: ")
                    session.add(User(username=username, email=email))
                    user = session.query(User).filter_by(
                        username=username).scalar()
                    session.add(
                        Profile(bio=bio, phone=phone, user_id=user.user_id))
                    print("User is successfully created.")

            case "add-task" | "at":
                task_title = input("Task's title: ")
                task_description = input("Task's description: ")
                session.add(
                    Task(title=task_title, description=task_description))
                print("Task is successfully created.")

            case "add-project" | "ap":
                task_title = input("Task's title: ")
                task_description = input("Task's description: ")
                session.add(
                    Task(title=task_title, description=task_description))

            case "del-user" | "du":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    session.delete(user)
                    session.delete(user.profile)
                else:
                    print("User is not defined.")

            case "del-task" | "dt":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(User, int(task_id))
                if task is not None:
                    session.delete(task)
                else:
                    print("Task is not defined.")

            case "del-project" | "dpj":
                while not (project_id := input("Task's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                project = session.get(User, int(project_id))
                if project:
                    session.delete(project)
                else:
                    print("User is not defined.")

            case "upt-email" | "ue":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    new_email = input("New user's email: ")
                    if session.query(User).filter_by(email=new_email).count() > 0:
                        print("User with this email already exists.")
                    else:
                        user.email = new_email
                else:
                    print("User is not defined.")

            case "upt-phone" | "up":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    phone = input("New user's phone number: ")
                    if session.query(User).filter_by(email=new_email).count() > 0:
                        print("User with this phone number already exists.")
                    else:
                        user.profile.phone = phone
                else:
                    print("User is not defined.")

            case "upt-bio" | "ub":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    bio = input("New user's biography: ")
                    user.profile.bio = bio
                else:
                    print("User is not defined.")

            case "upt-task-desc" | "utd":
                while not (project_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(User, int(task_id))

                if task is not None:
                    task.description = input("New task's description: ")
                else:
                    print("Task is not defined.")

            case "upt-task-title" | "utt":
                while not (project_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(User, int(task_id))

                if task is not None:
                    task.title = input("New task's title: ")
                else:
                    print("Task is not defined.")

            case "upt-status" | "us":
                while not (project_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(User, int(task_id))

                if task is not None:
                    task.status = input("Task's status: ")
                else:
                    print("Task is not defined.")

            case "upt-project-desc" | "upd":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                task = session.get(User, int(task_id))

                if task is not None:
                    task.description = input("New project's description: ")
                else:
                    print("Project is not defined.")

            case "upt-project-title" | "upt":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                task = session.get(User, int(task_id))

                if task is not None:
                    task.title = input("New project's title: ")
                else:
                    print("Project is not defined.")

            case "quit" | "q" | "exit" | "ex":
                break

            case _:
                sim_cmd = difflib.get_close_matches(cmd, COMMANDS)
                pprint(f"Unknown command \"{cmd}\".")
                if len(sim_cmd) > 0:
                    print("Probably you meant:", ", ".join(sim_cmd))

        session.commit()


if __name__ == "__main__":
    main()
