## This program allows the user to login based on usernames and passwords stored in a separate file.
## If login is successful, the user is presented with options to view tasks info stored in another separate file.
## The admin user has additional options that allow for registering new users and viewing statistics.


#=====importing libraries===========
from datetime import time
from datetime import datetime
from tabulate import tabulate

#====Functions Section====
class Task():

    def __init__(self, assigned, title, description, due, date_assigned, complete):
        self.assigned = assigned
        self.title = title
        self.description = description
        self.due = due
        self.date_assigned = date_assigned
        self.complete = complete

    def mark_complete(self):
        self.complete = "Yes"

def user_dict():
    file_list = []
    try:
        with open('user.txt', 'r+') as f:
            for line in f:
                split_list = line.split(", ")
                split_list[1] = split_list[1].strip("\n")
                file_list.append(tuple(split_list))
        user_dict = dict(file_list)
    except FileNotFoundError:
        print("File not found. Check filename and directory location. Try again.")
    return user_dict

def validate_login(name, pw):
    try:
        login_dict = user_dict()
        checked_name = False
        stored_pw = login_dict[name]
        checked_name = True
    except KeyError:
        print("Username does not exist. Please try again.")

    checked_pw = False
    if checked_name:
        if pw == stored_pw:
            print("Login successful!")
            checked_pw = True
        else:
            print("Incorrect password. Please try again.")

    if checked_pw and checked_name:
        login_passed = True
    else:
        login_passed = False

    return login_passed

def format_info(contents,index):
    try:
        content_list = contents.split(", ")
        to_print = f'''\n[Task index number {index}: {content_list[1]}]
        Assigned to:        {content_list[0]}
        Task description:   {content_list[2]}
        Due Date:           {content_list[3]}
        Task assigned on    {content_list[4]}
        Completion:         {content_list[5]}'''
    except IndexError:
        to_print = f"Task index number {index} does not contain all the necessary information."
    return to_print

def reg_user():
    try_again = True
    while try_again:
        try:
            new_name = input("New username (case sensitive): ").strip()
            login_dict = user_dict()
            existing_pw = login_dict[new_name]
            print(f"{new_name} already exists, with password: {existing_pw}\nTry a different username.")
            try_again = True
        except KeyError:
            new_pw = input("New password (case sensitive): ").strip()
            confirm_pw = input("Re-enter password (case sensitive): ").strip()
            if new_pw == confirm_pw:
                with open('user.txt', 'a+') as f:
                    f.write(f"\n{new_name}, {new_pw}")
                    print("New user registered successfully!")
            else:
                print("The passwords do not match. Please try again.")
            try_again = False
    return

def add_task():
    try:
        user_name = input("Username of person the task is assigned to: ").strip()
        title = input("Task title: ").strip()
        description = input("Task description: ").strip()
        due_date = input("Task due date (dd/mm/yyyy): ").strip()
        entry_date = str(time.today().strptime('%d/%m/%Y'))
        task_complete = "No"

        with open('tasks.txt', 'a+') as f:
            f.write(f"\n{user_name}, {title}, {description}, {due_date}, {entry_date}, {task_complete}")
        print("New task added succesfully!")

    except Exception:
        print("Something went wrong. Try again.")
    return

def view_all():
    try:
        with open('tasks.txt', 'r+') as f:
            count = 0
            for line in f:
                count += 1
                print(format_info(line, count))
    except FileNotFoundError:
        print("File not found. Check filename and try again.")
    return

def view_mine():
    try_again = True
    while try_again:
        try:
            task_list = task_objects()
            print(f"\n--- Tasks for {input_name} ---\n")
            count = 0
            for index in range(len(task_list)):
                if task_list[index].assigned == input_name:
                    task = task_list[index]
                    line = f"{task.assigned}, {task.title}, {task.description}, {task.due}, {task.date_assigned}, {task.complete}"
                    count += 1
                    print(format_info(line, index))
            
            # selecting task number to modify, or return to menu
            selecting = True
            while selecting:
                try:
                    selection = int(input(f"\nEnter a task index number to edit, or -1 to return to the main menu: "))
                    if selection != -1 and task_list[selection].assigned == input_name:
                        
                        editing = True
                        while editing:
                            edit = input('''
                            What do you want to edit?
                                m - mark as complete
                                u - username
                                d - due date
                                e - exit
                            : ''')
                            
                            if edit =='m':
                                task_list[selection].mark_complete()
                                update_task_file(task_list)
                                print("Task marked as complete!")
                            
                            elif edit == 'u':
                                if task_list[selection].complete == 'No':
                                    task_list[selection].assigned = input("New username assigned to: ").strip()
                                    update_task_file(task_list)
                                    print("New username saved!")
                                else:
                                    print("Task has been marked complete. No longer able to edit.")
                            
                            elif edit == 'd':
                                if task_list[selection].complete == 'No':
                                    task_list[selection].due = input("New due date: ").strip()
                                    update_task_file(task_list)
                                    print("New due date saved!")
                                else:
                                    print("Task has been marked complete. No longer able to edit.")

                            elif edit == 'e':
                                editing = False
                            
                            else:
                                print("Invalid entry. Try again.")
                        
                        selecting = False
                    
                    elif selection == -1:
                        selecting = False
                        try_again = False
                    
                    else:
                        print("Invalid entry. Try again.")

                except ValueError:
                    print("Invalid entry. Try again")
                except IndexError:
                    print("You have selected an invalid task number. Try again.")

            if count == 0:
                print("No tasks found.\n")
                try_again = False

        except FileNotFoundError:
            print("File not found. Check filename and try again.")
    return

def generate_reports():
    login_dict = user_dict()
    task_list = task_objects()

# --- task_oveview.txt ---
    num_total = len(task_list)

    num_completed = 0
    for task in task_list:
        if task.complete == 'Yes':
            num_completed += 1

    num_incomplete = num_total - num_completed

    num_overdue = 0
    for task in task_list:
        if task.complete != 'Yes' and datetime.strptime(task.due, '%d/%m/%Y') < datetime.now():
            num_overdue += 1
    
    pct_incomplete = num_incomplete / num_total * 100
    pct_overdue = num_overdue / num_total * 100

    with open('task_overview.txt', 'w+')as f:
        f.write(f'''
Total tasks:      {num_total}
Total completed:  {num_completed}
Total incomplete: {num_incomplete}
Total overdue:    {num_overdue}
% incomplete:     {round(pct_incomplete,1)}%
% overdue:        {round(pct_overdue,1)}%''')

# --- user_oveview.txt ---
    user_total = len(login_dict)
    table = []
    for key in login_dict:

        complete = 0
        overdue = 0
        residual = 0
        for task in task_list:
            if task.assigned == key:
                if task.complete == "Yes":
                    complete += 1
                elif task.complete != 'Yes' and datetime.strptime(task.due, '%d/%m/%Y') < datetime.now():
                    overdue += 1
                else:
                    residual += 1

        total = complete + overdue + residual
        if total != 0:
            table.append([
                key,
                total, 
                round(total/num_total*100,1), 
                round(complete/total*100,1), 
                round((overdue+residual)/total*100,1), 
                round(overdue/total*100,1)
                ])
        else:
            table.append([
                key,
                total,
                '-',
                '-',
                '-',
                '-',
            ])

    headers = [
        'Username', 
        'Total tasks', 
        '% of all tasks assigned to username', 
        '% completed',
        '% incomplete',
        '% overdue'
        ]

    with open('user_overview.txt', 'w+') as f:
        f.write(f'''
Total users:        {user_total}
Total tasks:        {num_total}

{tabulate(table, headers)}
        ''')

    return

def display_statistics():
    try:
        content = ''
        with open('task_overview.txt', 'r+') as f:
            for line in f:
                content += line
        with open('user_overview.txt', 'r+') as f:
            for line in f:
                content += line
        print(content)

    except FileNotFoundError:
        generate_reports()
        content = ''
        
        with open('task_overview.txt', 'r+') as f:
            for line in f:
                content += line
        with open('user_overview.txt', 'r+') as f:
            for line in f:
                content += line
        print(content)
    return

def task_objects():
    try:
        with open('tasks.txt', 'r+') as f:
            task_list = []
            for line in f:
                task = line.strip("\n").split(", ")
                task_list.append(Task(task[0], task[1], task[2], task[3], task[4], task[5]))
    except FileNotFoundError:
            print("File not found. Check filename and try again.")
    return task_list

def update_task_file(task_list):
    try:
        contents = ""
        for task in task_list:
            contents += f"{task.assigned}, {task.title}, {task.description}, {task.due}, {task.date_assigned}, {task.complete}\n"

        with open('tasks.txt', 'w+') as f:
            f.write(contents)

    except FileNotFoundError:
            print("File not found. Check filename and try again.")
    return


#====Login Section====
try_again = True
while try_again:
    input_name = input("Username (case sensitive): ").strip()
    input_pw = input("Password (case sensitive): ").strip()
    login_passed = validate_login(input_name, input_pw)
    try_again = not login_passed


#====Options Section====
while login_passed:
    if input_name == 'admin':
        menu = input('''\nSelect one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics 
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    : ''').lower()

    if menu == 'r' and input_name == 'admin':   # allows only the admin to register new users.
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'gr' and input_name == 'admin': # only the admin user has this option:
        generate_reports()

    elif menu == 'ds' and input_name == 'admin': # only the admin user has this option
        display_statistics()

    elif menu == 'e':
        print('Goodbye!')
        exit()

    else:
        print("You have made a wrong choice. Please try again.")