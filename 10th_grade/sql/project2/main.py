"""Module provides beautiful printing tables"""
import os
import difflib

from sqlalchemy import or_
from sqlalchemy.orm.session import Session as SessionType
from tabulate import tabulate

from db import Session
from db.models import Task, Profile, Project, User, association_table


COMMANDS = [
    "add-user", "au", "add-task", "at",
    "add-project", "ap", "del-user", "du",
    "del-task", "dt", "del-project", "dp",
    "upt-email", "ue", "upt-phone", "up",
    "upt-bio", "ub", "upt-task-desc", "utd",
    "upt-task-title", "utt", "upt-status", "us",
    "upt-project-desc", "upd", "upt-project-title", "upt",
    "reassign-task", "rt", "reassign-user", "ru",
    "search-user", "su", "find-user", "fu",
    "search-task", "st", "find-task", "ft",
    "search-project", "sp", "find-project", "fp",
    "project-tasks", "pt", "project-users", "pu",
    "user-tasks", "ut", "quit", "q", "exit", "ex"
]


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

    welcome()

    while user_input := input(">>> "):
        pprint(end="")
        cmd = user_input
        match cmd:
            case "add-user" | "au":
                username = input("User's username: ")
                email = input("User's email: ")

                if session.query(User).filter_by(email=email).count() > 0:
                    print("User with this email already exists.")
                elif session.query(User).filter_by(username=username).count() > 0:
                    print("User with this username already exists.")
                else:
                    bio = input("Profile's biography: ")
                    phone = input("Profile's phone number: ")
                    session.add(User(username=username, email=email))
                    user = session.query(User).filter_by(
                        username=username).scalar()

                    session.add(Profile(
                        bio=bio,
                        phone=phone,
                        user_id=user.id)
                    )
                    print("User is successfully created.")

            case "add-task" | "at":
                task_title = input("Task's title: ")

                if session.query(Task).filter_by(title=task_title).count() > 0:
                    print("Task with this title already exists.")
                    continue

                task_description = input("Task's description: ")

                if not task_description:
                    task_description = None

                if session.query(Project).filter_by(title=task_title).count() > 0:
                    print("Project with this title already exists.")

                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                if session.get(Project, int(project_id)) is not None:
                    session.add(Task(
                        title=task_title,
                        description=task_description,
                        status="N",
                        project_id=int(project_id)
                    ))
                    print("Task is successfully created.")
                else:
                    print("Project is not defined.")

            case "add-project" | "ap":
                project_title = input("Project's title: ")
                if session.query(Project).filter_by(title=project_title).count() > 0:
                    print("Project with this title already exists.")
                else:
                    project_description = input("Project's description: ")

                    if not project_description:
                        project_description = None

                    session.add(Project(
                        title=project_title,
                        description=project_description)
                    )
                    print("Project is successfully created.")

            case "del-user" | "du":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                profile = session.get(Profile, int(user_id))
                if profile is not None:
                    session.delete(profile)
                    session.delete(profile.user)
                    print("User is successfully deleted.")
                else:
                    print("User is not defined.")

            case "del-task" | "dt":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))
                if task is not None:
                    session.delete(task)
                    print("Task is successfully deleted.")
                else:
                    print("Task is not defined.")

            case "del-project" | "dp":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                project = session.get(Project, int(project_id))
                if project is not None:
                    tasks = project.tasks
                    for task in tasks:
                        session.delete(task)

                    session.delete(project)
                    print("Project is successfully deleted.")
                else:
                    print("Project is not defined.")

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
                        print("Email is successfully updated.")
                else:
                    print("User is not defined.")

            case "upt-phone" | "up":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(Profile, int(user_id))
                if user is not None:
                    phone = input("New user's phone number: ")
                    if session.query(Profile).filter_by(phone=phone).count() > 0:
                        print("User with this phone number already exists.")
                    else:
                        user.phone = phone
                        print("Phone is successfully updated.")
                else:
                    print("User is not defined.")

            case "upt-bio" | "ub":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    bio = input("New user's biography: ")
                    user.profile.bio = bio
                    print("Biography is successfully updated.")
                else:
                    print("User is not defined.")

            case "upt-task-desc" | "utd":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    task.description = input("New task's description: ")
                    print("Description is successfully updated.")
                else:
                    print("Task is not defined.")

            case "upt-task-title" | "utt":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    task_title = input("New task's title: ")

                    if session.query(Task).filter_by(title=task_title).count() > 0:
                        print("Task with this title already exists.")
                    else:
                        task.title = task_title
                        print("Task's title is successfully updated.")
                else:
                    print("Task is not defined.")

            case "upt-status" | "us":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    task.status = input("Task's status: ")
                    print("Status is successfully updated.")
                else:
                    print("Task is not defined.")

            case "upt-project-desc" | "upd":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))

                if project is not None:
                    project.description = input("New project's description: ")
                else:
                    print("Project is not defined.")

            case "upt-project-title" | "upt":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))

                if project is not None:
                    project_title = input("New project's title: ")

                    if session.query(Project).filter_by(title=project_title).count() > 0:
                        print("Task with this title already exists.")
                    else:
                        project.title = project_title
                        print("Project's title is successfully updated.")
                else:
                    print("Project is not defined.")

            case "reassign-task" | "rt":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    while not (project_id := input("Project's id: ")).isdecimal():
                        print("Project-id must be integer, try again.")

                    if session.get(Project, int(project_id)) is not None:
                        task.project_id = project_id
                        print("Task is successfully reassigned to another project.")
                    else:
                        print("Project is not defined.")
                else:
                    print("Task is not defined.")

            case "reassign-user" | "ru":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                if session.get(User, int(user_id)) is not None:
                    while not (project_id := input("Project's id: ")).isdecimal():
                        print("Project-id must be integer, try again.")

                    if session.get(Project, int(project_id)) is not None:
                        insert_stmt = association_table.insert().values(
                            user_id=user_id, project_id=project_id)
                        session.execute(insert_stmt)
                        print("User is successfully reassigned to another project.")
                    else:
                        print("Project is not defined.")
                else:
                    print("Task is not defined.")

            case "search-user" | "su" | "find-user" | "fu":
                pattern = input("Your request: ")
                found = session.query(Profile).filter(
                    or_(
                        User.username.like(f"%{pattern}%"),
                        User.email.like(f"%{pattern}%"),
                        Profile.bio.like(f"%{pattern}%"),
                        Profile.phone.like(f"%{pattern}%")
                    )
                ).all()
                print(tabulate(
                    [(profile.id, profile.user.username, profile.user.email, profile.phone)
                     for profile in found],
                    headers=['Id', 'Username', 'Email', 'Phone'],
                    tablefmt='rounded_grid')
                )

            case "search-task" | "st" | "find-task" | "ft":
                pattern = input("Your request: ")
                found = session.query(Task).filter(
                    or_(
                        Task.description.like(f"%{pattern}%"),
                        Task.title.like(f"%{pattern}%")
                    )
                ).all()
                print(tabulate(
                    [(task.id, task.title, task.project_id, task.status)
                     for task in found],
                    headers=['Id', 'Title', 'Project-ID', 'Status'],
                    tablefmt='rounded_grid')
                )

            case "search-project" | "sp" | "find-project" | "fp":
                pattern = input("Your request: ")
                found = session.query(Project).filter(
                    or_(
                        Project.description.like(f"%{pattern}%"),
                        Project.title.like(f"%{pattern}%")
                    )
                ).all()
                print(tabulate(
                    [(project.id, project.title)
                     for project in found],
                    headers=['Id', 'Title'],
                    tablefmt='rounded_grid')
                )

            case "project-tasks" | "pt":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))
                if project is not None:
                    tasks = project.tasks
                    print(tabulate(
                        [(task.id, task.title, task.project_id, task.status)
                         for task in tasks],
                        headers=['Id', 'Title', 'Project-ID', 'Status'],
                        tablefmt='rounded_grid')
                    )
                else:
                    print("Project is not defined.")

            case "project-users" | "pu":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))
                if project is not None:
                    users = project.users
                    print(tabulate(
                        [(user.id, user.user.username, user.user.email, user.phone)
                         for user in users],
                        headers=['Id', 'Username', 'Email', 'Phone'],
                        tablefmt='rounded_grid')
                    )

            case "user-tasks" | "ut":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(Profile, int(user_id))
                if user is not None:
                    tasks = user.tasks
                    print(tabulate(
                        [(task.id, task.title, task.project_id, task.status)
                         for task in tasks],
                        headers=['Id', 'Title', 'Project-ID', 'Status'],
                        tablefmt='rounded_grid')
                    )
                else:
                    print("Project is not defined.")

            case "quit" | "q" | "exit" | "ex":
                break

            case _:
                sim_cmd = difflib.get_close_matches(cmd, COMMANDS, cutoff=0.75)
                pprint(f"Unknown command \"{cmd}\".")
                if len(sim_cmd) > 0:
                    print("Probably you meant:", ", ".join(sim_cmd))

        session.commit()

    session.close()


if __name__ == "__main__":
    main()
