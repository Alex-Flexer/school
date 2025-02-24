COMMANDS = [
    "add-user", "ad", "add-task", "at",
    "add-project", "ap", "del-user", "du",
    "del-task", "dt", "del-project", "dp",
    "upd-email", "ue", "upd-phone", "up",
    "upd-bio", "ub", "upd-task-desc", "utd",
    "upd-task-title", "utt", "upd-status", "us",
    "upd-project-desc", "upd", "upd-project-title", "upt",
    "reassign-task", "rast", "assign-user", "asu",
    "search-user", "su", "find-user", "fu",
    "search-task", "st", "find-task", "ft",
    "search-project", "sp", "find-project", "fp",
    "project-tasks", "pt", "project-users", "pu",
    "unassign-user", "unasu", "user-projects", "upj",
    "quit", "q", "exit", "ex", "all-users", "all-tasks",
    "all-projects", "alu", "alt", "alp"
]

HELP_DESCRIPTION = """Instruction:


add-user (ad) — Adds a new user to the system.

add-task (at) — Creates a new task to be completed.

add-project (ap) — Adds a new project to the system.

del-user (du) — Removes a user from the system.

del-task (dt) — Deletes a task from the system.

del-project (dp) — Deletes a project from the system.

upd-email (ue) — Updates the email address of a user.

upd-phone (up) — Updates the phone number of a user.

upd-bio (ub) — Updates the biography or additional information about a user.

upd-task-desc (utd) — Updates the description of a task.

upd-task-title (utt) — Updates the title of a task.

upd-status (us) — Updates the status of a task ("N", "P", "R", "T", "D").

upd-project-desc (upd) — Updates the description of a project.

upd-project-title (upt) — Updates the title of a project.

reassign-task (rast) — Reassigns a task to another project.

assign-user (asu) — Assigns a user to a project.

unassign-user (unasu) — Unassigns a user from a project.

search-user (su) — Searches for a user based on specified criteria.

find-user (fu) — Alternative command for searching for a user.

search-task (st) — Searches for a task based on specified criteria.

find-task (ft) — Alternative command for searching for a task.

search-project (sp) — Searches for a project based on specified criteria.

find-project (fp) — Alternative command for searching for a project.

project-tasks (pt) — Displays a list of tasks associated with a specific project.

project-users (pu) — Displays a list of users working on a specific project.

user-projects (upj) — Displays a list of projects in which a specific user is involved.

all-users (alu) — Displays a list of all users in the system.

all-tasks (alt) — Displays a list of all tasks in the system.

all-projects (alp) — Displays a list of all projects in the system.

quit (q) — Exits the service.

exit (ex) — Alternative command for exiting the service.
"""


VALIDATE_PHONE_NUMBER_PATTERN =\
    "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"


WELCOME_TEXT = """Welcome to Flexer-Manager-System!
To get instruction use \"help\" (h)
"""
