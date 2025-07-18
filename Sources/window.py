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
    root.overrideredirect(True)
    root.title("Scan Main Serial")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    # root.protocol("WM_DELETE_WINDOW", lambda: None)
    w, h = 850, 450
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_hight = root.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_hight // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    
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
        if all(serials):
            result["value"] = serials
            root.quit()
            root.destroy()
        else:
            label_error.config(text="Please Keys all Sub Serials")
    def on_quit():
        result["value"] = "back"
        root.quit()
        root.destroy()
    root = tk.Tk()
    root.overrideredirect(True)
    root.title("Scan Sub Serials")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    # root.protocol("WM_DELETE_WINDOW", lambda: None)
    w, h = 850, 450
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_hight = root.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_hight // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # ✅ ให้ root ยืดหยุ่นเมื่อถูก resize
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # ✅ สร้าง frame สำหรับเนื้อหากลาง
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    # ✅ ให้ frame ยืดแนวตั้งแนวนอน
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    # ✅ หัวข้อ
    tk.Label(frame, text="Scan Sub Serials", font=("Helvetica", 32)).grid(
        row=0, column=0, columnspan=2, pady=(0, 20)
    )
    entry_list = []
    for i, name in enumerate(sub_names):
        tk.Label(frame, text=name + ":", font=("Helvetica", 20), anchor="e").grid(
            row=i + 1, column=0, sticky="e", padx=10, pady=5
        )
        entry = tk.Entry(frame, font=("Helvetica", 20), width=30)
        entry.grid(row=i + 1, column=1, sticky="w", padx=10, pady=5)
        entry.bind("<Return>", lambda e, idx=i: entry_list[idx + 1].focus_set() if idx + 1 < len(sub_names) else on_submit())
        entry_list.append(entry)
    entry_list[0].focus_set()
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.grid(row=len(sub_names) + 1, column=0, columnspan=2, pady=5)
    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=len(sub_names) + 2, column=0, columnspan=2, pady=10)
    tk.Button(btn_frame, text="Apply", command=on_submit, font=("Helvetica", 24), width=10).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Back", command=on_quit, font=("Helvetica", 24), width=10).pack(side="left", padx=10)
    root.mainloop()
    return result["value"]

def message_popup(type, header, message):
    print("Header")
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    if type == 1:
        messagebox.showinfo(header, message)
    elif type == 2:
        messagebox.showwarning(header, message)
    elif type == 3:
        messagebox.showerror(header, message)

# print(scan_sub_serial(["BN Screw", "Interface PBA SN"]))
# scan_main_serial("IN700")
# message_popup(3, "HI", "HELLO WORLD")