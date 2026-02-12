import os
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox,PhotoImage

# ================== CONFIG =================
APP_ICON = "ico/app_icon"

PRIMARY = "#6C63FF"
SECONDARY = "#1E1E2F"
CARD = "#2A2D3E"
ACCENT = "#00D4FF"
TEXT = "#FFFFFF"

# ================= FUNCIONES =================
def rename_videos(folder, base_name, start_chapter, extension):
    files = [f for f in os.listdir(folder) if f.lower().endswith(extension.lower())]
    files.sort()

    chapter = start_chapter
    for file in files:
        old_path = os.path.join(folder, file)
        new_name = f"{base_name}_Chapter_{chapter}{extension}"
        new_path = os.path.join(folder, new_name)

        os.rename(old_path, new_path)
        add_log(f"✔ {file}  →  {new_name}")
        chapter += 1

    status_var.set("Completed successfully 🚀")

def add_log(text):
    log_text.insert(tk.END, text + "\n")
    log_text.see(tk.END)

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def run_rename():
    status_var.set("Processing...")

    folder = folder_var.get().strip()
    base = base_var.get().strip()
    ext = ext_var.get().strip()

    try:
        chapter = int(chapter_var.get())
    except:
        messagebox.showerror("Error", "Chapter must be numeric")
        return

    if not folder or not base or not ext:
        messagebox.showerror("Error", "All fields required")
        return

    rename_videos(folder, base, chapter, ext)

# ================= GUI =================
root = tk.Tk()
root.title(" Video Renamer Pro")

# Icono ventana
try:
    if platform.system() == "Windows":
        root.iconbitmap(f"{APP_ICON}.ico") 
        # Usa .ico en Windows 
    else: 
        icon_img = PhotoImage(file=f"{APP_ICON}.png") 
        # Usa .png en Linux 
        root.iconphoto(True, icon_img)
except:
    pass

root.geometry("760x560")
root.configure(bg=SECONDARY)
root.minsize(620, 480)

# ================= STYLE =================
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=10,
                background=PRIMARY,
                foreground="white",
                borderwidth=0)

style.map("TButton",
          background=[("active", "#5A54D6")])

style.configure("TEntry",
                padding=6,
                fieldbackground="#1B1D2A",
                foreground="white")

# ================= VARIABLES =================
folder_var = tk.StringVar()
base_var = tk.StringVar()
chapter_var = tk.StringVar(value="1")
ext_var = tk.StringVar(value=".mp4")
status_var = tk.StringVar(value="Ready")

# ================= MENÚ =================
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(
    label="About",
    command=lambda: messagebox.showinfo(
        "About",
        "🎬 Video Renamer Pro\n\nCreator: Carlos Filgueira"
    )
)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# ================= GRID RESPONSIVE =================
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# ================= CARD FRAME =================
form_frame = tk.LabelFrame(root,
                           text=" ⚙ Configuration ",
                           bg=CARD,
                           fg="white",
                           font=("Segoe UI", 11, "bold"),
                           padx=15,
                           pady=15)

form_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
form_frame.columnconfigure(1, weight=1)

# ================= CAMPOS =================
def label(text, row):
    tk.Label(form_frame,
             text=text,
             bg=CARD,
             fg="white",
             font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=6)

def entry(var, row, width=40):
    e = ttk.Entry(form_frame, textvariable=var, width=width)
    e.grid(row=row, column=1, sticky="ew", pady=6)
    return e

label("📂 Folder", 0)
entry(folder_var, 0)
ttk.Button(form_frame, text="Browse", command=select_folder).grid(row=0, column=2, padx=8)

label("📝 Base Name", 1)
entry(base_var, 1)

label("🔢 Start Chapter", 2)
entry(chapter_var, 2, 10)

label("📄 Extension", 3)
entry(ext_var, 3, 10)

# ================= BOTÓN CON ANIMACIÓN =================
action_frame = tk.Frame(root, bg=SECONDARY)
action_frame.grid(row=1, column=0, pady=10)

rename_btn = ttk.Button(action_frame, text="🚀 Rename Videos", command=run_rename)
rename_btn.pack(ipadx=20, ipady=5)

def animate_hover(event):
    rename_btn.configure(style="Hover.TButton")

def animate_leave(event):
    rename_btn.configure(style="TButton")

style.configure("Hover.TButton",
                background=ACCENT,
                foreground="black")

rename_btn.bind("<Enter>", animate_hover)
rename_btn.bind("<Leave>", animate_leave)

# ================= LOG =================
log_frame = tk.LabelFrame(root,
                          text=" 📜 Activity Log ",
                          bg=CARD,
                          fg="white",
                          font=("Segoe UI", 11, "bold"))

log_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
log_frame.columnconfigure(0, weight=1)
log_frame.rowconfigure(0, weight=1)

log_text = tk.Text(log_frame,
                   bg="#181A24",
                   fg="#EAEAF0",
                   font=("Consolas", 10),
                   relief="flat")

scroll = ttk.Scrollbar(log_frame, command=log_text.yview)
log_text.configure(yscrollcommand=scroll.set)

log_text.grid(row=0, column=0, sticky="nsew")
scroll.grid(row=0, column=1, sticky="ns")

# ================= STATUS BAR =================
status_bar = tk.Label(root,
                      textvariable=status_var,
                      bg="#14151D",
                      fg="#AAAAAA",
                      anchor="w",
                      padx=10)

status_bar.grid(row=3, column=0, sticky="ew")

# ================= MAIN LOOP =================
root.mainloop()
