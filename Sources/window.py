import os
import tkinter as tk
from tkinter import messagebox
from fitsdll import fn_Handshake

def scan_main_serial(operation, model= "*"):
    def on_submit():
        serial = entry.get().strip()

        if len(serial) == 12:
            status = fn_Handshake(model, operation, serial)
            if status == True:
                result.set(serial)
                root.destroy()
            else:
                label_error.config(text=status)
        else:
            label_error.config(text="Serial must be 12 digit")
    def on_quit():
        print("User close program")
        root.destroy()
        os._exit(0)

    root = tk.Tk()
    root.title("Scan Main Serial")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    result = tk.StringVar()
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text="Please scan Main Serial (12 Digit):", font=("Helvetica", 32)).pack(pady=20)
    entry = tk.Entry(frame, font=("Courier", 36), justify="center")
    entry.pack(pady=20)
    entry.focus()
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.pack()
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=30)
    tk.Button(button_frame, text="Apply", font=("Helvetica", 24), width=10, command=on_submit).pack(side="left", padx=20)
    tk.Button(button_frame, text="Cancal", font=("Helvetica", 24), width=10, command=on_quit).pack(side="right", padx=20)
    root.mainloop()

    return result.get()

def scan_sub_serial(num_serials=2):
    def on_submit():
        entries_values = [e.get().strip() for e in entry_list]
        if all(val for val in entries_values):
            result.set(entries_values)
            root.destroy()
        else:
            label_error.config(text="Please fill all Sub Serial")
    def on_quit():
        print("Exit Sub Serial")
        root.quit()
    root = tk.Tk()
    root.title("Scan Sub Serials")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    result = tk.StringVar()
    entry_list = []
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text=f"Please scan Sub Serial", font=("Helvetica", 32)).pack(pady=20)
    for i in range(num_serials):
        row = tk.Frame(frame)
        row.pack(pady=10)
        tk.Label(row, text=f"Sub Serial {i + 1}:", font=("Helvetica", 28)).pack(side="left", padx=10)
        entry = tk.Entry(row, font=("Courier", 36), justify="center", width=20)
        entry.pack(side="left")
        if i == 0:
            entry.focus()
        entry_list.append(entry)
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.pack()
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=30)
    tk.Button(button_frame, text="Apply", font=("Helvetica", 24), width=10, command=on_submit).pack(side="left", padx=20)
    tk.Button(button_frame, text="Cancal", font=("Helvetica", 24), width=10, command=on_quit).pack(side="right", padx=20)
    root.mainloop()
    return result.get()

print(scan_sub_serial(2)[1])