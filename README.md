# Task Manager
Task Manager is a Python program that manages assignments and deadlines for tasks using Tkinter GUI.

## Getting Started
### Requirements
- Python compiler or IDE

### Installing
The program is one file, but it will automatically create a second file named 'tasks.csv' in the same directory.
Do not delete this file, or it will reset all data in the program.
Loading a different data set into the program will work,
but change the 'data_file' name to match at the top of the program.

### Execution
Simply run main.py using whatever your preferred method is.
The program will open a new GUI window to operate the program.

## Functionality
### Creating New Tasks
To create a new task, enter a name into the *New Task* bar and enter a due date.
This due date will always be either 'today' or within the next year, including leap year adjustment.

You may also enter a weight into the weight bar. Any numeric weighting system you like will work;
it may, however, change the priorities in the algorithm.
I recommend integer weights in the range [-2, 3] unless there is a task that requires more extreme numbers.
Entering a weight is not required to create a new task, but if none is entered,
or if the entered weight is not a number, the program will set the weight to 0.

Once all fields are entered as desired, press the *Add Task* button.
If the task name already exists or the date is invalid, the task will not be created.
Note that the task will automatically be converted to title case,
meaning the first letter of every word will be uppercase and all others lowercase.

### Task Search
To filter tasks by class, search for a specific type of work, or just look up any word pattern,
type it into the *Task Keywords* box and press *Search.* The program will filter the list of tasks
and update the task dropdown with the tasks relating to the search.

To clear the selection and show all tasks in the dropdown, press the *Clear* button.
Pressing *Clear* will also remove the task in the dropdown.

### Viewing and Updating Task Status
To view or update the status of a task, first select it in the dropdown.
The current status will show up at the top of the page as well as lighting up in the status buttons below.
To view all information about the task, (weight, created/due dates, etc) click the *View* button.

To change the status of the selected task, click on any of the status buttons below, then click the *Update* button.
If *Finished* was selected, the task will be removed from the task list, so be careful!

Statuses are numbered in the data file: 0 for Not Started, 1 for In Progress, 2 for Reviewing.
This comes into play in the algorithm.

### Find a Task
The colored buttons at the bottom all show display windows based on the following:

***View All Tasks:*** Shows a popup window of all tasks arranged alphabetically

***Random Task:*** Generates a completely random task from the list. Basically roll a die

***Algorithm Task:*** Generates a task from the following elimination algorithm:

Priorities:
- Due date is today or it's overdue
- Due date is tomorrow or day after and weight > 0
- Highest number of 3\*weight + 3\*status - days_until_due

Tiebreakers:
- Largest weight
- Largest status number
- Percentage of the way done
- Added to the task list first

### Data
All activity is automatically saved to the specified txt files in the folder. (default name: tasks.csv)
There are 5 columns the program uses to filter data: name, weight, created_date, due_date, status.
If you want to load a new task set, make sure it is a dataset with those five column names in that order.

## Author
Shawn Mastandrea

## Version History
- v1 : October 2026
    - Initial GitHub release

## License
This project is licensed under an MIT license - see the LICENSE.md file for details
