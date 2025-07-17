import os
import tkinter as tk
from tkinter import messagebox
from fitsdll import fn_Handshake

def scan_main_serial(operation, model= "*"):
    result = {"value": None}

    def on_submit():
        serial = entry.get().strip()

        if len(serial) == 12:
            status = fn_Handshake(model, operation, serial)
            if status == True:
                result["value"] = serial
                root.quit()
                root.destroy()
            else:
                label_error.config(text=status)
        else:
            label_error.config(text="Serial must be 12 digit")
    def on_quit():
        result["value"] = "quit"
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Scan Main Serial")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text=f"Operation {operation}\nPlease scan Main Serial (12 Digit):", font=("Helvetica", 32)).pack(pady=20)
    entry = tk.Entry(frame, font=("Courier", 36), justify="center")
    entry.pack(pady=20)
    entry.focus_set()
    root.bind("<Return>", lambda event: on_submit())
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.pack()
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=30)
    tk.Button(button_frame, text="Apply", font=("Helvetica", 24), width=10, command=on_submit).pack(side="left", padx=20)
    tk.Button(button_frame, text="Quit", font=("Helvetica", 24), width=10, command=on_quit).pack(side="right", padx=20)
    root.mainloop()
    return result["value"]

def scan_sub_serial(sub_names: list):
    if len(sub_names) == 0:
        return None
    
    result = {"value": None}

    def on_submit():
        serials = [entry.get().strip() for entry in entry_list]
        if all(serials):  # ตรวจว่าทุกช่องมีข้อมูล
            result["value"] = serials
            root.quit()
            root.destroy()
        else:
            label_error.config(text="กรุณากรอกให้ครบทุกช่อง")
    def on_quit():
        result["value"] = "back"
        root.quit()
        root.destroy()
    
    root = tk.Tk()
    root.title("Scan Sub Serials")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    entry_list = []
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text="Please scan all Sub Serial", font=("Helvetica", 32)).pack(pady=20)
    for name in sub_names:
        row = tk.Frame(frame)
        row.pack(pady=10)
        tk.Label(row, text=f"{name}:", font=("Helvetica", 28)).pack(side="left", padx=10)
        entry = tk.Entry(row, font=("Courier", 36), justify="center", width=20)
        entry.pack(side="left")
        entry_list.append(entry)
    entry_list[0].focus()
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.pack()
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=30)
    tk.Button(button_frame, text="Apply", font=("Helvetica", 24), width=10, command=on_submit).pack(side="left", padx=20)
    tk.Button(button_frame, text="Back", font=("Helvetica", 24), width=10, command=on_quit).pack(side="right", padx=20)
    root.mainloop()
    return result["value"]

def message_popup(type, header, message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    if type == 1:
        messagebox.showinfo(header, message)
    elif type == 2:
        messagebox.showwarning(header, message)
    elif type == 2:
        messagebox.showerror(header, message)

# print(scan_sub_serial(["BN Screw"]))
# scan_main_serial("IN700")