import tkinter as tk
from tkinter import messagebox
from fitsdll import fn_Handshake, fn_Query

def scan_serial(mode: str, model: str, operation: str, sub_names: list):
    main_result = {}

    def on_submit():
        sub_serial = "" 
        serial = entry.get().strip()
        if mode.upper() == "PRODUCTION":
            if len(serial) == 12:
                status = fn_Handshake(model, operation, serial)
                if status is True:
                    main_result["main"] = serial
                    sub_serial = scan_sub_serial(root, sub_names)
                    if operation == "IN240":
                        if sub_serial[1][:3] == "CIB":
                            status = fn_Query("Interface connector", "IC200", sub_serial[1], "Result")
                            if status == "PASS":
                                main_result["subs"] = sub_serial
                                root.quit()
                                root.destroy()
                            else:
                                messagebox.showwarning("Handcheck Fail", f"Serial: {sub_serial[1]}\nMust be key Operation IC200 before use!!" )
                                return
                        else:
                            messagebox.showwarning("Invalid serial", """Interface connector must be start with "CIB" """)
                            return
                    else:
                        main_result["subs"] = sub_serial
                        root.quit()
                        root.destroy()

                elif sub_serial == "back":
                    entry.delete(0, tk.END)
                    entry.focus_set()
                    return

                else:
                    label_error.config(text=status)
            else:
                label_error.config(text="Serial must be 12 digit")
        else:
            main_result["main"] = serial
            sub_serial = scan_sub_serial(root, sub_names)
            if sub_serial == "back":
                main_result["main"] = None
                main_result["subs"] = None
                entry.delete(0, tk.END)
                label_error.config(text="")
                entry.focus_set()
                return
            main_result["subs"] = sub_serial
            root.quit()
            root.destroy()
            
    def on_quit():
        main_result["main"] = "quit"
        main_result["subs"] = "quit"
        root.quit()
        root.destroy()

    root = tk.Tk()
    # root.overrideredirect(True)
    root.title("Scan Main Serial")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    w, h = 850, 450
    # root.geometry(f"{w}x{h}")
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
    return main_result

def scan_sub_serial(root, sub_names: list):
    if len(sub_names) == 0:
        return None
    result = {"value": None}
    def on_submit():
        serials = [entry.get().strip() for entry in entry_list]
        if all(serials):
            result["value"] = serials
            sub.destroy()
        else:
            label_error.config(text="Please Keys all Sub Serials")
    def on_quit():
        result["value"] = "back"
        sub.destroy()
    sub = tk.Toplevel(root)
    sub.overrideredirect(True)
    sub.title("Scan Sub Serials")
    sub.resizable(False, False)
    sub.lift()
    sub.attributes("-topmost", True)
    w, h = 850, 450
    sub.update_idletasks()
    screen_width = sub.winfo_screenwidth()
    screen_height = sub.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    sub.geometry(f"{w}x{h}+{x}+{y}")
    frame = tk.Frame(sub)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
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
        entry.bind("<Return>", lambda e, idx=i: entry_list[idx + 1].focus_set()
                   if idx + 1 < len(sub_names) else on_submit())
        entry_list.append(entry)
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.grid(row=len(sub_names) + 1, column=0, columnspan=2, pady=5)
    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=len(sub_names) + 2, column=0, columnspan=2, pady=10)
    tk.Button(btn_frame, text="Apply", command=on_submit, font=("Helvetica", 24), width=10).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Back", command=on_quit, font=("Helvetica", 24), width=10).pack(side="left", padx=10)
    sub.after_idle(lambda: entry_list[0].focus_force())
    # ✅ ทำให้หน้าต่างนี้ modal → block root
    sub.grab_set()
    root.wait_window(sub)
    # ✅ return ค่าที่ถูกตั้งไว้ใน result
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

# serial, subs = scan_serial("PRODUCTION", "Main line", "IN240", ["BN Screw", "Interface PBA SN"])
# print(serial)
# print(subs)