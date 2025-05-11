import tkinter as tk
import subprocess

# Module launch functions
def open_bankers():
    subprocess.Popen(["python", "BankersAlgorithm.py"])

def open_rag():
    subprocess.Popen(["python", "module3_rag_cycle.py"])

def open_wait_for_graph():
    subprocess.Popen(["python", "waitforgraphs.py"])

def open_deadlock_resolver():
    subprocess.Popen(["python", "deadlock_resolver.py"])

# Create main window
root = tk.Tk()
root.title("🧠 OS Algorithm Visualizer")
root.attributes('-fullscreen', True)
root.configure(bg="#f8f9fa")

# Exit fullscreen on Escape
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

# Title label
tk.Label(
    root,
    text="🧠 OS Algorithms Visualizer Hub",
    font=("Helvetica", 32, "bold"),
    bg="#f8f9fa",
    fg="#2c3e50"
).pack(pady=50)

# Button container
btn_frame = tk.Frame(root, bg="#f8f9fa")
btn_frame.pack(pady=20)

# Utility to create buttons
def create_button(text, command, bg):
    return tk.Button(
        btn_frame,
        text=text,
        command=command,
        font=("Arial", 16, "bold"),
        width=35,
        height=2,
        bg=bg,
        fg="white",
        activebackground="#2c3e50",
        activeforeground="white",
        bd=0,
        relief="raised",
        cursor="hand2"
    )

# Add styled buttons
create_button("💡 Banker's Algorithm Visualizer", open_bankers, "#4CAF50").pack(pady=15)
create_button("🧮 RAG Deadlock Detector", open_rag, "#2196F3").pack(pady=15)
create_button("🔗 Wait-For Graph Visualizer", open_wait_for_graph, "#9C27B0").pack(pady=15)
create_button("🛡️ Deadlock Resolver & Timeline", open_deadlock_resolver, "#FF7043").pack(pady=15)

# Footer
tk.Label(
    root,
    text="Press ESC to exit fullscreen | Made by Varshitha © 2025",
    font=("Arial", 11),
    bg="#f8f9fa",
    fg="#7f8c8d"
).pack(side="bottom", pady=20)

root.mainloop()
