import tkinter as tk
from tkinter import ttk
import datetime as dt
import pandas as pd
from numpy import max, select
from random import randint

data_file = 'tasks.csv'

def write():
    df.to_csv(data_file, index=False)

try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=['name', 'weight', 'created_date', 'due_date', 'status'])
    write()
date_format = df.loc[:, 'created_date']
df['created_date'] = [dt.datetime.strptime(day, "%Y-%m-%d").date() for day in date_format]
date_format = df.loc[:, 'due_date']
df['due_date'] = [dt.datetime.strptime(day, "%Y-%m-%d").date() for day in date_format]

active_task = None

def max_day(month: int, year: int):
    match month:
        case 2:
            return 28 + (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        case 4 | 6 | 9 | 11:
            return 30
        case _:
            return 31

# frame
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x300")
main_frame = tk.Frame(root)
main_frame.grid(column=0, row=0, sticky="nsew")

close_button = tk.Button(main_frame, text='CLOSE', command=root.destroy, fg='firebrick', font=('Arial', 12, 'bold'))
close_button.grid(column=0, row=0, padx=5, pady=5, sticky='nw')

# action display widget (row 1)
display = tk.Label(main_frame, text='Welcome to Task Manager!', font=('Arial', 12, 'bold'), fg='white')
display.grid(column=0, row=1, columnspan=2, padx=5, pady=10, sticky='nw')

# new task (row 2)
new_task_frame = tk.Frame(main_frame)
new_task_frame.grid(column=0, row=2, sticky='nw')
new_task_row1 = tk.Frame(new_task_frame)
new_task_row1.grid(column=0, row=0, sticky='nw')
new_task_row2 = tk.Frame(new_task_frame)
new_task_row2.grid(column=0, row=1, sticky='nw')

def new_task():
    name = new_task_name.get().title()
    try:
        weight = int(new_task_weight.get()) or 0
    except ValueError:
        weight = 0
    if not name:
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='Please enter a task name!')
        return
    if name in df['name'].tolist():
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text=f'{name} already exists!')
        return
    else:
        date = dt.date.today()
        try:
            month = int(new_task_month.get())
            day = int(new_task_day.get())
            if 1 <= month <= 12 and 1 <= day <= max_day(month, dt.date.today().year + 1):
                date = date.replace(month=month, day=day)
                if dt.date.today() > date:
                    date = date.replace(year=date.year + 1)
                new_row = [name, weight, dt.date.today(), date, 0]
                df.loc[len(df)] = new_row
                write()
                display['fg'] = 'limegreen'
                display.config(text=f'Added {name} to task list to do by {date:%B %d, %Y}')
                new_task_name.delete(0, 'end')
                new_task_weight.delete(0, 'end')
                new_task_month.delete(0, 'end')
                new_task_day.delete(0, 'end')
                select_dropdown.config(values=df['name'].tolist())
                return
        except ValueError:
            pass
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='Please enter a valid todo by date!')

# new task widgets (row 2)
new_task_title_label = tk.Label(new_task_row1, text="New Task:")
new_task_title_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
new_task_name = tk.Entry(new_task_row1, width=20)
new_task_name.grid(column=1, row=0, sticky='w')
new_task_weight_label = tk.Label(new_task_row1, text='Weight')
new_task_weight_label.grid(column=2, row=0, sticky='w')
new_task_weight = tk.Entry(new_task_row1, width=2)
new_task_weight.grid(column=3, row=0, sticky='w')
new_task_todo_by_label = tk.Label(new_task_row2, text="Todo By:")
new_task_todo_by_label.grid(column=0, row=0, padx=5, sticky='w')
new_task_month = tk.Entry(new_task_row2, width=2)
new_task_month.grid(column=1, row=0, sticky='w')
new_task_date_separator_label = tk.Label(new_task_row2, text="/")
new_task_date_separator_label.grid(column=2, row=0, sticky='w')
new_task_day = tk.Entry(new_task_row2, width=2)
new_task_day.grid(column=3, row=0, sticky='w')
add_task_button = tk.Button(new_task_row2, text="Add Task", command=new_task, fg='green')
add_task_button.grid(column=4, row=0, padx=5, sticky="w")

# task search dropdown (row 3)
search_frame = tk.Frame(main_frame)
search_frame.grid(column=0, row=3, pady=10, sticky='nw')

task_list = df['name'].tolist()
def on_select_dropdown(event=None):
    global active_task
    active_task = select_dropdown.get()
    status = df[df['name'] == active_task]['status'].tolist()[0]
    match status:
        case 0:
            status_press_0()
            display['fg'] = 'plum'
            display.config(text=f'{active_task} is currently Not Started.')
        case 1:
            status_press_1()
            display['fg'] = 'lightblue'
            display.config(text=f'{active_task} is currently In Progress.')
        case 2:
            status_press_2()
            display['fg'] = 'orange'
            display.config(text=f'{active_task} is currently in Reviewing.')

def reset_select_dropdown():
    global active_task, current_status
    select_dropdown.set('Choose a Task...')
    active_task = None
    current_status = -1

def apply_keywords():
    keyword = select_search_bar.get()
    if not not keyword:
        filtered = [item for item in df['name'] if keyword.lower() in item.lower()]
        select_dropdown.config(values=filtered)
        display['fg'] = 'orange' if not filtered else 'lightblue'
        display.config(text=f'{len(filtered)} task{'' if len(filtered) == 1 else 's'} found containing {keyword}')
        select_dropdown.config(values=filtered)
        status_reset()
        reset_select_dropdown()
    else:
        clear_keywords()

def clear_keywords():
    select_search_bar.delete(0, 'end')
    select_dropdown.config(values=df['name'].tolist())
    display['fg'] = 'goldenrod' if display['fg'] == 'yellow' else 'yellow'
    display.config(text='Keyword clear')
    reset_select_dropdown()

select_keyword_label = tk.Label(search_frame, text='Task Keywords:')
select_keyword_label.grid(column=0, row=0, padx=5, sticky='w')
select_search_bar = tk.Entry(search_frame, width=13)
select_search_bar.grid(row=0, column=1, sticky='w')
select_search_apply_button = tk.Button(search_frame, command=apply_keywords,
                                       fg='purple', text='Search', font=('Arial', 12, 'normal'))
select_search_apply_button.grid(row=0, column=2, sticky='w')
search_clear_button = tk.Button(search_frame, command=clear_keywords,
                                fg='#503000', text='Clear', font=('Arial', 12, 'normal'))
search_clear_button.grid(row=0, column=3, sticky='w')

def update_task():
    global df, active_task
    if active_task is not None and current_status != -1:
        display['fg'] = ('plum', 'lightblue', 'orange', 'limegreen')[current_status]
        display.config(text=f'{active_task} is now marked as {
        ('Not Started.', 'In Progress.', 'Reviewing.', 'done!')[current_status]}')
        index = df.index[df['name'] == active_task].tolist()[0]
        if current_status == 3:
            df = df.drop(index)
            status_reset()
            select_dropdown.set('Choose a Task...')
            select_dropdown.config(values=df['name'].tolist())
            active_task = None
        else:
            df.iloc[index, 4] = current_status
        write()
    else:
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='Please choose a task to update!')

def view_task():
    row1 = df[df['name'] == active_task]
    try:
        row = row1.iloc[0].tolist()
    except IndexError:
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='Please choose a task to view!')
        return
    display['fg'] = 'gray' if display['fg'] == 'lightgray' else 'lightgray'
    display.config(text=f'Viewing {active_task}...')
    task_popup_window = tk.Toplevel(root)
    task_popup_window.title(active_task)
    task_popup_window.geometry('300x200')

    close_window_button = tk.Button(task_popup_window, text='CLOSE', command=task_popup_window.destroy,
                                    fg='firebrick', font=('Arial', 12, 'bold'))
    close_window_button.grid(column=0, row=0, padx=5, pady=5, sticky='nw')
    text = f'''
    {row[0]}\n{row[1]} Weight\nAdded {row[2]}\nDue {row[3]}
    Currently {('Not Started', 'In Progress', 'Under Review')[row[4]]}'''
    random_task_textbox = tk.Label(task_popup_window, text=text)
    random_task_textbox.grid(column=0, row=1, padx=5, pady=5, sticky='n')

# dynamic dropdown based on search (row 4)
dropdown_frame = tk.Frame(main_frame)
dropdown_frame.grid(column=0, row=4, padx=5, sticky='nw')
select_dropdown = ttk.Combobox(dropdown_frame, values=df['name'].tolist(), state='readonly')
select_dropdown.set('Choose a Task...')
select_dropdown.grid(row=0, column=0)
select_dropdown.bind('<<ComboboxSelected>>', on_select_dropdown)
update_button = tk.Button(dropdown_frame, command=update_task, text='Update', font=('Arial', 12, 'bold'))
update_button.grid(row=0, column=1)
view_button = tk.Button(dropdown_frame, command=view_task, text='View', font=('Arial', 12, 'bold'))
view_button.grid(row=0, column=2)

current_status = -1

# update and edit task status (rows 5 and 6)
def status_press_0():
    if active_task is not None:
        global current_status
        current_status = 0
        status_button_0['fg'] = 'red'
        status_button_0.config(font=('Arial', 12, 'bold'))
        status_button_1['fg'] = 'black'
        status_button_1.config(font=('Arial', 12, 'normal'))
        status_button_2['fg'] = 'black'
        status_button_2.config(font=('Arial', 12, 'normal'))
        status_button_3['fg'] = 'black'
        status_button_3.config(font=('Arial', 12, 'normal'))
def status_press_1():
    if active_task is not None:
        global current_status
        current_status = 1
        status_button_1['fg'] = 'blue'
        status_button_1.config(font=('Arial', 12, 'bold'))
        status_button_0['fg'] = 'black'
        status_button_0.config(font=('Arial', 12, 'normal'))
        status_button_2['fg'] = 'black'
        status_button_2.config(font=('Arial', 12, 'normal'))
        status_button_3['fg'] = 'black'
        status_button_3.config(font=('Arial', 12, 'normal'))
def status_press_2():
    if active_task is not None:
        global current_status
        current_status = 2
        status_button_2['fg'] = 'orange'
        status_button_2.config(font=('Arial', 12, 'bold'))
        status_button_0['fg'] = 'black'
        status_button_0.config(font=('Arial', 12, 'normal'))
        status_button_1['fg'] = 'black'
        status_button_1.config(font=('Arial', 12, 'normal'))
        status_button_3['fg'] = 'black'
        status_button_3.config(font=('Arial', 12, 'normal'))
def status_press_3():
    if active_task is not None:
        global current_status
        current_status = 3
        status_button_3['fg'] = 'green'
        status_button_3.config(font=('Arial', 12, 'bold'))
        status_button_0['fg'] = 'black'
        status_button_0.config(font=('Arial', 12, 'normal'))
        status_button_1['fg'] = 'black'
        status_button_1.config(font=('Arial', 12, 'normal'))
        status_button_2['fg'] = 'black'
        status_button_2.config(font=('Arial', 12, 'normal'))

# status update widgets (rows 5 and 6)
status_frame = tk.Frame(main_frame)
status_frame.grid(column=0, row=5, padx=5, pady=5, sticky='nw')
status_button_0 = tk.Button(status_frame, text='Not Started', command=status_press_0, font=('Arial', 12, 'normal'))
status_button_0.grid(row=0, column=0, sticky='w')
status_button_1 = tk.Button(status_frame, text='In Progress', command=status_press_1, font=('Arial', 12, 'normal'))
status_button_1.grid(row=0, column=1, sticky='w')
status_button_2 = tk.Button(status_frame, text='Reviewing', command=status_press_2, font=('Arial', 12, 'normal'))
status_button_2.grid(row=0, column=2, sticky='w')
status_button_3 = tk.Button(status_frame, text='Finished', command=status_press_3, font=('Arial', 12, 'normal'))
status_button_3.grid(row=0, column=3, sticky='w')

def status_reset():
    """Resets all status buttons to their default, non-lit state."""
    status_button_0['fg'] = 'black'
    status_button_0.config(font=('Arial', 12, 'normal'))
    status_button_1['fg'] = 'black'
    status_button_1.config(font=('Arial', 12, 'normal'))
    status_button_2['fg'] = 'black'
    status_button_2.config(font=('Arial', 12, 'normal'))
    status_button_3['fg'] = 'black'
    status_button_3.config(font=('Arial', 12, 'normal'))

# generate task button functions
def view_all_tasks():
    if len(df) == 0:
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='There are currently no tasks!')
        return

    task_popup_window = tk.Toplevel(root)
    task_popup_window.title('All Tasks')
    task_popup_window.geometry('300x200')

    close_window_button = tk.Button(task_popup_window, text='CLOSE', command=task_popup_window.destroy,
                                    fg='firebrick', font=('Arial', 12, 'bold'))
    close_window_button.grid(column=0, row=0, padx=5, pady=5, sticky='nw')
    task_list_view = df['name'].tolist()
    all_tasks_textbox = tk.Label(task_popup_window, text='\n' + '\n'.join(sorted(task_list_view)))
    all_tasks_textbox.grid(column=0, row=1, padx=5, pady=5, sticky='n')

def random_task():
    """Generates a random task in a popup window."""
    if len(df) == 0:
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='There are currently no tasks!')
        return

    index = randint(0, len(df) - 1)
    task_popup_window = tk.Toplevel(root)
    task_popup_window.title('Random Task')
    task_popup_window.geometry('300x200')

    close_window_button = tk.Button(task_popup_window, text='CLOSE', command=task_popup_window.destroy,
                                    fg='firebrick', font=('Arial', 12, 'bold'))
    close_window_button.grid(column=0, row=0, padx=5, pady=5, sticky='nw')
    row = df.iloc[index, :].tolist()
    text = f'''
    {row[0]}\n{row[1]} Weight\nAdded {row[2]}\nDue {row[3]}
    Currently {('Not Started', 'In Progress', 'Under Review')[row[4]]}'''
    random_task_textbox = tk.Label(task_popup_window, text=text)
    random_task_textbox.grid(column=0, row=1, padx=5, pady=5, sticky='n')

def algorithm_task():
    """Calculates the 'best' task to do at the moment, algorithmically. Displays the task in a popup window.\n
    Priorities: due today or overdue, then due date is tomorrow or day after and weight > 0, then:\n
    3*weight + 3*status - days_until_due\n
    Tiebreakers: largest weight, largest status, percentage of the way done, lowest index in the list"""
    if len(df) == 0:
        display['fg'] = 'crimson' if display['fg'] == 'red' else 'red'
        display.config(text='There are currently no tasks!')
        return

    task_popup_window = tk.Toplevel(root)
    task_popup_window.title('Algorithm Task')
    task_popup_window.geometry('300x200')

    dfa = df.copy()
    conditions = [dfa['due_date'] <= dt.date.today(),
                  (dfa['due_date'] - dfa['created_date'] <= dt.timedelta(days=2)) & (dfa['weight'] > 0)]
    dfb = [dfa[col].tolist() for col in ['weight', 'created_date', 'due_date', 'status']]
    dfa.loc[:, 'default'] = [3*(dfb[0][i] + dfb[3][i]) - (dfb[2][i] - dt.date.today()).days for i in range(len(dfa))]
    dfa.loc[:, 'priority'] = select(conditions, [.1, .2], default=dfa['default'])

    index = -1
    final = dfa.loc[dfa['priority'] == .1, :]
    if len(final) == 0:
        final = dfa.loc[dfa['priority'] == .2, :]
        if len(final) == 0:
            dpm = max(dfa['priority'])
            final = dfa.loc[dfa['priority'] == dpm, :]
    # tiebreakers
    if len(final) > 1:
        fwm = max(final['weight'])
        final = final.loc[final['weight'] == fwm, :]
        if len(final) > 1:
            fsm = max(final['status'])
            final = final.loc[final['status'] == fsm, :]
            if len(final) > 1:
                due_date = final['due_date'].tolist()
                created_date = final['created_date'].tolist()
                final.loc[:, 'percentage'] = [((due - dt.date.today()).days + 0.1) / ((due - created).days + 1)
                                              for due, created in zip(due_date, created_date)]
                print(final)
    index = final.index[0] if index == -1 else index

    close_window_button = tk.Button(task_popup_window, text='CLOSE', command=task_popup_window.destroy,
                                    fg='firebrick', font=('Arial', 12, 'bold'))
    close_window_button.grid(column=0, row=0, padx=5, pady=5, sticky='nw')
    row = df.iloc[index].tolist()
    text = f'''
    {row[0]}\n{row[1]} Weight\nAdded {row[2]}\nDue {row[3]}
    Currently {('Not Started', 'In Progress', 'Under Review')[row[4]]}'''
    random_task_textbox = tk.Label(task_popup_window, text=text)
    random_task_textbox.grid(column=0, row=1, padx=5, pady=5, sticky='n')

# generate task buttons (row 7)
generate_task_frame = tk.Frame(main_frame)
view_all_tasks_button = tk.Button(generate_task_frame, text='View All Tasks', command=view_all_tasks,
                                  font=('Arial', 12, 'bold'), fg='#807730')
view_all_tasks_button.grid(column=0, row=0, sticky='w')
generate_task_frame.grid(column=0, row=6, padx=5, pady=5, sticky='nw')
random_task_button = tk.Button(generate_task_frame, text='Random Task', command=random_task,
                               font=('Arial', 12, 'bold'), fg='coral')
random_task_button.grid(column=1, row=0, sticky='w')
algorithm_task_button = tk.Button(generate_task_frame, text='Algorithm Task', command=algorithm_task,
                                  font=('Arial', 12, 'bold'), fg='midnightblue')
algorithm_task_button.grid(column=2, row=0, sticky='w')

root.mainloop()
