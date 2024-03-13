from tkinter import *
import tkinter.messagebox
from datetime import datetime, timedelta

# Create the main window
window = Tk()
window.title("To-Do List")

# Create a dictionary to store task creation times, completion status, and priority
task_creation_times = {}
task_completion_status = {}
task_priority = {}

# Function to add a task and check for overdue tasks
def add_task():
    task_text = entry_task.get()
    if task_text:
        current_time = datetime.now()
        task_creation_times[task_text] = current_time
        task_completion_status[task_text] = False
        task_priority[task_text] = priority_var.get()
        # Insert tasks in a sorted order based on priority
        tasks_sorted = sorted(task_creation_times.keys(), key=lambda x: task_priority[x])
        listbox_tasks.delete(0, END)  # Clear the listbox
        for task in tasks_sorted:
            listbox_tasks.insert(END, f"{task} - Priority: {task_priority[task]} - {task_creation_times[task].strftime('%Y-%m-%d %H:%M:%S')}")
        entry_task.delete(0, "end")
        check_overdue_tasks()

def delete_task():
    selected_task = listbox_tasks.get(ANCHOR).split(" - ")[0]
    del task_creation_times[selected_task]
    del task_completion_status[selected_task]
    del task_priority[selected_task]
    listbox_tasks.delete(ANCHOR)

def mark_as_read():
    selected_task = listbox_tasks.get(ANCHOR).split(" - ")[0]
    task_completion_status[selected_task] = True
    # Update the listbox display after marking task as read
    listbox_tasks.delete(ANCHOR)
    listbox_tasks.insert(END, f"{selected_task} - Priority: {task_priority[selected_task]} - {task_creation_times[selected_task]} (Completed)")

def view_task():
    selected_task = listbox_tasks.get(ANCHOR).split(" - ")[0]
    task_details = f"Task: {selected_task}\nPriority: {task_priority[selected_task]}\nCreated: {task_creation_times[selected_task]}\nStatus: {'Completed' if task_completion_status[selected_task] else 'Not Completed'}"
    tkinter.messagebox.showinfo("Task Details", task_details)

def check_overdue_tasks():
    current_time = datetime.now()
    for task, creation_time in task_creation_times.items():
        if (current_time - creation_time) > timedelta(hours=24):
            tkinter.messagebox.showwarning("Task Overdue", f"The task '{task}' is overdue!")

def search_task():
    search_text = entry_search.get().lower()
    listbox_tasks.delete(0, END)
    for task, creation_time in task_creation_times.items():
        if search_text in task.lower():
            listbox_tasks.insert(END, f"{task} - Priority: {task_priority[task]} - {creation_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Entry and buttons
entry_task = Entry(window, width=40)
entry_task.pack(pady=10)

# Priority dropdown
priority_var = StringVar(window)
priority_var.set("Low")  # Default priority
priority_label = Label(window, text="Priority:")
priority_label.pack()
priority_dropdown = OptionMenu(window, priority_var, "Low", "Medium", "High")
priority_dropdown.pack()

add_button = Button(window, text="Add Task", width=40, command=add_task)
add_button.pack()

delete_button = Button(window, text="Delete Task", width=40, command=delete_task)
delete_button.pack()

mark_as_read_button = Button(window, text="Mark as Read", width=40, command=mark_as_read)
mark_as_read_button.pack()

view_task_button = Button(window, text="View Task", width=40, command=view_task)
view_task_button.pack()

# Search functionality
entry_search = Entry(window, width=40)
entry_search.pack(pady=10)
search_button = Button(window, text="Search Task", width=40, command=search_task)
search_button.pack()

# Listbox for tasks
listbox_tasks = Listbox(window, bg="lavender", fg="black", height=15, width=50, font="Helvetica")
listbox_tasks.pack()

# Check for overdue tasks when the application starts
check_overdue_tasks()

window.mainloop()