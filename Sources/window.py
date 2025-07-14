import os
import tkinter as tk
from tkinter import messagebox
from fitsdll import fn_Handshake

def scan_main_serial_fullscreen(operation, model= "*"):
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

def scan_sub_serial_fullscreen(serial_length=12):
    def on_submit():
        sub1 = entry1.get().strip()
        sub2 = entry2.get().strip()
        if len(sub1) == serial_length and len(sub2) == serial_length:
            result.set((sub1, sub2))
            root.destroy()
        else:
            label_error.config(
                text=f"both Sub-Serial must be {serial_length} digit"
            )
    def on_quit():
        print("👋 ออกจากหน้าสแกน Sub Serial")
        root.destroy()
        os._exit(0)

    root = tk.Tk()
    root.title("Scan Sub Serials")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    result = tk.StringVar()
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text="Please scan Sub-Serials", font=("Helvetica", 32)).pack(pady=20)
    # ✅ แถว Sub Serial 1
    row1 = tk.Frame(frame)
    row1.pack(pady=10)
    tk.Label(row1, text="Sub Serial 1:", font=("Helvetica", 28)).pack(side="left", padx=10)
    entry1 = tk.Entry(row1, font=("Courier", 36), justify="center", width=20)
    entry1.pack(side="left")
    entry1.focus()
    # ✅ แถว Sub Serial 2
    row2 = tk.Frame(frame)
    row2.pack(pady=10)
    tk.Label(row2, text="Sub Serial 2:", font=("Helvetica", 28)).pack(side="left", padx=10)
    entry2 = tk.Entry(row2, font=("Courier", 36), justify="center", width=20)
    entry2.pack(side="left")
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.pack()
    # ✅ ปุ่มกด
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=30)
    tk.Button(button_frame, text="Apply", font=("Helvetica", 24), width=10, command=on_submit).pack(side="left", padx=20)
    tk.Button(button_frame, text="cancal", font=("Helvetica", 24), width=10, command=on_quit).pack(side="right", padx=20)
    root.mainloop()
    return result.get()

def message_popup(type, header, message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    if type == 1:
        messagebox.showinfo(header, message)
    if type == 2:
        messagebox.showwarning(header, message)
    if type == 3:
        messagebox.showerror(header, message)