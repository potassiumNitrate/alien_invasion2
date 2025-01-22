import tkinter as tk
root = tk.Tk()
root.title("Tkinter 示例")
root.geometry("400x200")
entry = tk.Entry(root, width=300)
entry.pack(pady=1)
root.mainloop()