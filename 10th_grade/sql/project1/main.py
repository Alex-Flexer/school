from db.models import Database


def wecome():
    print("welcome!\nInstruction:...")

def main():
    db_path = "./tasks.db"
    db = Database(db_path)

    welcome()

    while user_input := input():
        args = user_input.split()
        match args[0]:
            case "create" | "cr":
                name = args[1]
                desc = " ".join(args[2:])
                task_table.objects.create(name, desc)
            case "all" | "a":
                tasks = task_table.objects.all()
                print(f"Found {len(tasks)} task(s)")
                for task in tasks:
                    print(
                        f"name: {task[0]}, description: '{task[1]}', completed: {bool(task[2])}"
                    )
            case "find" | "search" | "f" | "s":
                pattern = " ".join(args[1:])
                tasks = task_table.objects.search(pattern)
                print(f"Found {len(tasks)} task(s)")
                for task in tasks:
                    print(
                        f"id: {task[0]}, name: {task[1]}, description: '{task[2]}', completed: {bool(task[3])}"
                    )

            case "complete" | "co" | "c":
                id = int(args[1])
                task_table.objects.complete(id)

            case "delete" | "d":
                id = int(args[1])
                task_table.objects.delete(id)

            case "quit" | "q" | "exit":
                break

            case _:
                raise ValueError("invalid command-line argument")


if __name__ == "__main__":
    d = Database('kasdf')
    # main()
