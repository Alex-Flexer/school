"""Main file"""
import os
import difflib
from platform import platform
import re

from sqlalchemy import or_, Table
from sqlalchemy.orm.session import Session as SessionType
from tabulate import tabulate

from db import Session
from db.models import Task, Profile, Project, User, association_table, Status
from config import (COMMANDS, HELP_DESCRIPTION,
                    VALIDATE_PHONE_NUMBER_PATTERN, WELCOME_TEXT)


TableType = Task | Profile | Project | User | Status | Table


assert len(set(COMMANDS)) == len(COMMANDS), "All commands should be unique."


def welcome():
    """Function print welcoming text"""
    pprint(WELCOME_TEXT)


def pprint(*args, **kwargs):
    """Function provides printing with clearing"""
    os.system("cls" if "windows" in platform().lower() else "clear")
    print(*args, **kwargs)


def check_entry_exists(session: SessionType, table: TableType, **kwargs) -> bool:
    """Function checks the presence of a entry in the table"""
    return session.query(table).filter_by(**kwargs).count() > 0


def check_entry_exists_by_id(session: SessionType, table: TableType, id_: int) -> bool:
    """Function checks the presence of a entry in the table by id"""
    return session.get(table, id_) is not None


def check_phone_number(phone_number: str) -> bool:
    """Function checks correctness of phone number"""
    return re.match(VALIDATE_PHONE_NUMBER_PATTERN, phone_number) is not None


def main():
    """Just main"""
    session: SessionType = Session()

    welcome()

    while user_input := input(">>> "):
        pprint(end="")
        cmd = user_input
        match cmd:
            case "add-user" | "au":
                username = input("User's username: ")
                email = input("User's email: ")

                if check_entry_exists(session, User, email=email):
                    print("User with this email already exists.")
                elif check_entry_exists(session, User, username=username):
                    print("User with this username already exists.")
                else:
                    bio = input("Profile's biography: ")
                    while not check_phone_number(phone := input("Profile's phone number: ")):
                        print("It does not look like a phone number, try again: ")

                    if not check_entry_exists(session, Profile, phone=phone):
                        session.add(User(username=username, email=email))
                        user = session.query(User).filter_by(
                            username=username).scalar()

                        session.add(Profile(
                            bio=bio,
                            phone=phone,
                            user_id=user.id)
                        )
                        print("User is successfully created.")
                    else:
                        print("User with this phone number already exists.")

            case "add-task" | "at":
                task_title = input("Task's title: ")

                if check_entry_exists(session, Task, title=task_title):
                    print("Task with this title already exists.")
                    continue

                task_description = input("Task's description (optional): ")

                if not task_description:
                    task_description = None

                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                if check_entry_exists_by_id(session, Project, int(project_id)):
                    status_id = session.query(Status).filter_by(
                        status='N').scalar().id
                    session.add(Task(
                        title=task_title,
                        description=task_description,
                        status_id=status_id,
                        project_id=int(project_id)
                    ))
                    print("Task is successfully created.")
                else:
                    print("Project is not defined.")

            case "add-project" | "ap":
                project_title = input("Project's title: ")

                if check_entry_exists(session, Project, title=project_title):
                    print("Project with this title already exists.")
                else:
                    project_description = input(
                        "Project's description (optional): ")

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

                user = session.get(User, int(user_id))
                if user is not None:
                    session.delete(user)
                    session.delete(user.profile)
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
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))
                if project is not None:
                    tasks = project.tasks
                    for task in tasks:
                        session.delete(task)

                    session.delete(project)
                    print("Project is successfully deleted.")
                else:
                    print("Project is not defined.")

            case "upd-email" | "ue":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    new_email = input("New user's email: ")
                    if check_entry_exists(session, User, email=new_email):
                        print("User with this email already exists.")
                    else:
                        user.email = new_email
                        print("Email is successfully updated.")
                else:
                    print("User is not defined.")

            case "upd-phone" | "up":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(Profile, int(user_id))
                if user is not None:
                    while not check_phone_number(phone := input("New phone number: ")):
                        print("It does not look like a phone number, try again: ")

                    if check_entry_exists(session, Profile, phone=phone):
                        print("User with this phone number already exists.")
                    else:
                        user.phone = phone
                        print("Phone is successfully updated.")
                else:
                    print("User is not defined.")

            case "upd-bio" | "ub":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    bio = input("New user's biography: ")
                    user.profile.bio = bio
                    print("Biography is successfully updated.")
                else:
                    print("User is not defined.")

            case "upd-task-desc" | "utd":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    task.description = input("New task's description: ")
                    print("Description is successfully updated.")
                else:
                    print("Task is not defined.")

            case "upd-task-title" | "utt":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    task_title = input("New task's title: ")

                    if check_entry_exists(session, Task, title=task_title):
                        print("Task with this title already exists.")
                    else:
                        task.title = task_title
                        print("Task's title is successfully updated.")
                else:
                    print("Task is not defined.")

            case "upd-status" | "us":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    task_status = input("Task's status: ")
                    new_status = session.query(Status).filter_by(
                        status=task_status).scalar()
                    if new_status is not None:
                        task.status_id = new_status.id
                        print("Status is successfully updated.")
                    else:
                        print("Unknown status.")
                else:
                    print("Task is not defined.")

            case "upd-project-desc" | "upd":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))

                if project is not None:
                    project.description = input(
                        "New project's description (optional): ")
                else:
                    print("Project is not defined.")

            case "upd-project-title" | "upt":
                while not (project_id := input("Project's id: ")).isdecimal():
                    print("Project-id must be integer, try again.")

                project = session.get(Project, int(project_id))

                if project is not None:
                    project_title = input("New project's title: ")

                    if check_entry_exists(session, Project, title=project_title):
                        print("Task with this title already exists.")
                    else:
                        project.title = project_title
                        print("Project's title is successfully updated.")
                else:
                    print("Project is not defined.")

            case "reassign-task" | "rast":
                while not (task_id := input("Task's id: ")).isdecimal():
                    print("Task-id must be integer, try again.")

                task = session.get(Task, int(task_id))

                if task is not None:
                    while not (project_id := input("Project's id: ")).isdecimal():
                        print("Project-id must be integer, try again.")

                    if check_entry_exists_by_id(session, Project, int(project_id)):
                        task.project_id = project_id
                        print("Task is successfully reassigned to another project.")
                    else:
                        print("Project is not defined.")
                else:
                    print("Task is not defined.")

            case "assign-user" | "asu":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                if check_entry_exists_by_id(session, User, int(user_id)):
                    while not (project_id := input("Project's id: ")).isdecimal():
                        print("Project-id must be integer, try again.")

                    if check_entry_exists_by_id(session, Project, int(project_id)):
                        if not check_entry_exists(
                                session, association_table,
                                project_id=project_id,
                                user_id=user_id):

                            insert_stmt = association_table.insert().values(
                                user_id=user_id,
                                project_id=project_id
                            )
                            session.execute(insert_stmt)
                            print("User is successfully assigned to this project.")
                        else:
                            print("This user is already assigned to this project.")
                    else:
                        print("Project is not defined.")
                else:
                    print("Task is not defined.")

            case "unassign-user" | "unasu":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                if check_entry_exists_by_id(session, User, int(user_id)):
                    while not (project_id := input("Project's id: ")).isdecimal():
                        print("Project-id must be integer, try again.")

                    if check_entry_exists_by_id(session, Project, int(project_id)):
                        if check_entry_exists(
                                session, association_table,
                                project_id=project_id,
                                user_id=user_id):

                            assoc_deletion = association_table.delete().where(
                                (association_table.c.user_id == user_id) &
                                (association_table.c.project_id == project_id)
                            )
                            session.execute(assoc_deletion)
                            print(
                                "User is successfully unassigned from this project.")
                        else:
                            print("This user is not assigned to this project.")
                    else:
                        print("Project is not defined.")
                else:
                    print("Task is not defined.")

            case "search-user" | "su" | "find-user" | "fu":
                pattern = input("Your request: ")
                found_profiles = session.query(Profile).filter(
                    or_(
                        Profile.bio.like(f"%{pattern}%"),
                        Profile.phone.like(f"%{pattern}%")
                    )
                ).all()

                found_users = session.query(User).filter(
                    or_(
                        User.username.like(f"%{pattern}%"),
                        User.email.like(f"%{pattern}%")
                    )
                ).all()

                users = set(
                    found_users +
                    [profile.user for profile in found_profiles]
                )
                table = [(user.id, user.username,
                          user.email, user.profile.phone)
                         for user in users]

                print(tabulate(
                    table,
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
                    [(task.id, task.title, task.project_id, task.status.status)
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
                        [(task.id, task.title, task.project_id, task.status.status)
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
                        [(user.id, user.username, user.email, user.profile.phone)
                         for user in users],
                        headers=['Id', 'Username', 'Email', 'Phone'],
                        tablefmt='rounded_grid')
                    )
                else:
                    print("Project is not defined.")

            case "user-projects" | "upj":
                while not (user_id := input("User's id: ")).isdecimal():
                    print("User-id must be integer, try again.")

                user = session.get(User, int(user_id))
                if user is not None:
                    projects = user.projects
                    print(tabulate(
                        [(project.id, project.title)
                         for project in projects],
                        headers=['Id', 'Title'],
                        tablefmt='rounded_grid')
                    )
                else:
                    print("User is not defined.")

            case "all-users" | "alu":
                users = [(user.id, user.username, user.email, user.profile.phone)
                         for user in session.query(User).all()]
                print(tabulate(
                    users,
                    headers=['Id', 'Username', 'Email', 'Phone'],
                    tablefmt='rounded_grid')
                )

            case "all-tasks" | "alt":
                tasks = [(task.id, task.title, task.project_id, task.status.status)
                         for task in session.query(Task).all()]
                print(tabulate(
                    tasks,
                    headers=['Id', 'Title', 'Project-ID', 'Status'],
                    tablefmt='rounded_grid')
                )

            case "all-projects" | "alp":
                projects = [(project.id, project.title)
                            for project in session.query(Project).all()]
                print(tabulate(
                    projects,
                    headers=['Id', 'Title'],
                    tablefmt='rounded_grid')
                )

            case "quit" | "q" | "exit" | "ex":
                break

            case "help" | "h":
                pprint(HELP_DESCRIPTION)

            case _:
                sim_cmd = difflib.get_close_matches(
                    cmd, COMMANDS, cutoff=0.75, n=3)
                pprint(f"Unknown command \"{cmd}\".")
                if len(sim_cmd) > 0:
                    print("Probably you meant:", ", ".join(sim_cmd))

        session.commit()

    session.close()


if __name__ == "__main__":
    main()
