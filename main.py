# Import necessary libraries
import os
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


# Function to enumerate files and folders in a directory and export them to a CSV file
def enumerate_files_and_folders(directory_path, csv_filename):
    # Open the CSV file for writing with UTF-8 encoding
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Full Path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Walk through the directory and its subdirectories
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                full_path = os.path.join(root, file)
                # Write file/folder name and its full path to the CSV
                writer.writerow({'Name': file, 'Full Path': full_path})


# Function to draw a tree structure of files and folders in a directory
def draw_tree(directory, parent_structure="", indent=""):
    tree_structure_text = indent + "---- " + os.path.basename(directory) + "\n"
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            tree_structure_text += draw_tree(os.path.join(root, dir), tree_structure_text, indent + "    ")
        for file in files:
            tree_structure_text += indent + "    ---- " + file + "\n"
    return tree_structure_text


# Function to open a file dialog and select a directory
def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, directory_path)


# Function to enumerate files and folders and export them when the corresponding button is clicked
def enumerate_and_export():
    directory_path = entry_path.get()
    if not directory_path:
        messagebox.showerror("Error", "Please select a directory.")
        return

    csv_filename = 'contents.csv'

    try:
        enumerate_files_and_folders(directory_path, csv_filename)
        messagebox.showinfo("Success", f"Enumeration completed. Results saved to {csv_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to view the tree structure when the corresponding button is clicked
def view_tree():
    directory_path = entry_path.get()
    if not directory_path:
        messagebox.showerror("Error", "Please select a directory.")
        return

    tree_structure = draw_tree(directory_path)

    # Create a new window to display the tree structure
    tree_window = tk.Toplevel(window)
    tree_window.title("Directory and File Tree")

    tree_text = tk.Text(tree_window, font=("Courier New", 10))
    tree_text.insert(tk.END, tree_structure)
    tree_text.pack()


# Create the main window
window = tk.Tk()
window.title("File and Folder Enumerator")

# Set window background color
window.configure(bg="#f0f0f0")

# Create and pack widgets with styling
label_path = tk.Label(window, text="Select a directory:", font=("Arial", 12))
label_path.pack(pady=10)

entry_path = tk.Entry(window, width=50, font=("Arial", 12))
entry_path.pack()

button_browse = tk.Button(window, text="Browse", command=browse_directory, font=("Arial", 12))
button_browse.pack(pady=10)

button_enumerate = tk.Button(window, text="Enumerate and Export", command=enumerate_and_export, font=("Arial", 12))
button_enumerate.pack()

button_view_tree = tk.Button(window, text="View Tree", command=view_tree, font=("Arial", 12))
button_view_tree.pack(pady=10)

# Start the GUI main loop
window.mainloop()
