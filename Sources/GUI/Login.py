import tkinter as tk

def scan_main_serial_fullscreen():
    def on_submit():
        serial = entry.get().strip()
        if len(serial) == 12:
            result.set(serial)
            root.destroy()
        else:
            label_error.config(text="Serial ต้องมี 12 หลัก")
    root = tk.Tk()
    root.title("Scan Main Serial")
    # ✅ ทำให้เต็มจอ + บนสุด + ไม่ให้ปิด
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # ห้ามปิดด้วย X
    result = tk.StringVar()
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text="กรุณากรอก Main Serial (12 หลัก):", font=("Helvetica", 32)).pack(pady=20)
    entry = tk.Entry(frame, font=("Courier", 36), justify="center")
    entry.pack(pady=20)
    entry.focus()
    label_error = tk.Label(frame, text="", font=("Helvetica", 20), fg="red")
    label_error.pack()
    tk.Button(frame, text="ตกลง", font=("Helvetica", 24), width=10, command=on_submit).pack(pady=30)
    root.mainloop()
    return result.get()

# ตัวอย่างเรียกใช้งาน
serial = scan_main_serial_fullscreen()
print("Main Serial:", serial)