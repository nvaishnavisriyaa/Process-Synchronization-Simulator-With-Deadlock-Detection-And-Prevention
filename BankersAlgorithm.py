import tkinter as tk
from tkinter import messagebox
import threading
import time

class ScrollableFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        canvas = tk.Canvas(self, height=800, width=1280)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class ProMaxBankersVisualizerScrollable:
    def __init__(self, master):
        self.master = master
        self.master.title("Banker's Algorithm - Pro Max Visualization (Scrollable)")
        self.scroll_frame = ScrollableFrame(master)
        self.scroll_frame.pack(fill="both", expand=True)

        self.process_boxes = []
        self.entries_allocation = []
        self.entries_maximum = []
        self.entries_available = []
        self.num_processes = 0
        self.num_resources = 0

        self.setup_ui()

    def setup_ui(self):
        frame = self.scroll_frame.scrollable_frame
        tk.Label(frame, text="Processes:", font=("Arial", 12)).grid(row=0, column=0)
        self.proc_entry = tk.Entry(frame, width=5)
        self.proc_entry.grid(row=0, column=1)

        tk.Label(frame, text="Resources:", font=("Arial", 12)).grid(row=0, column=2)
        self.res_entry = tk.Entry(frame, width=5)
        self.res_entry.grid(row=0, column=3)

        tk.Button(frame, text="Next", command=self.create_input_matrices, bg="#4CAF50", fg="white").grid(row=0, column=4)

        self.canvas = tk.Canvas(frame, width=1200, height=400, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas.grid(row=1, column=0, columnspan=10, pady=20)

        self.available_label = tk.Label(frame, text="", font=("Arial", 14, "bold"))
        self.available_label.grid(row=2, column=0, columnspan=10)

        self.status_text = tk.Text(frame, height=10, width=150, font=("Consolas", 10))
        self.status_text.grid(row=3, column=0, columnspan=10, pady=10)

        self.result_label = tk.Label(frame, text="", font=("Arial", 16, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=10, pady=10)

    def create_input_matrices(self):
        frame = self.scroll_frame.scrollable_frame
        try:
            self.num_processes = int(self.proc_entry.get())
            self.num_resources = int(self.res_entry.get())
        except:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return

        self.entries_allocation = []
        self.entries_maximum = []
        self.entries_available = []

        tk.Label(frame, text="Allocation Matrix", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=5)
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                e = tk.Entry(frame, width=4)
                e.grid(row=6 + i, column=j)
                row.append(e)
            self.entries_allocation.append(row)

        tk.Label(frame, text="Maximum Matrix", font=("Arial", 10, "bold")).grid(row=5, column=6, columnspan=5)
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                e = tk.Entry(frame, width=4)
                e.grid(row=6 + i, column=6 + j)
                row.append(e)
            self.entries_maximum.append(row)

        tk.Label(frame, text="Available:", font=("Arial", 10, "bold")).grid(row=6 + self.num_processes, column=0)
        for j in range(self.num_resources):
            e = tk.Entry(frame, width=4)
            e.grid(row=7 + self.num_processes, column=j)
            self.entries_available.append(e)

        tk.Button(frame, text="Start Visualization", command=self.start_visualization_thread, bg="#2196F3", fg="white").grid(row=8 + self.num_processes, column=0, columnspan=5)

    def start_visualization_thread(self):
        threading.Thread(target=self.visualize).start()

    def visualize(self):
        try:
            allocation = [[int(e.get()) for e in row] for row in self.entries_allocation]
            maximum = [[int(e.get()) for e in row] for row in self.entries_maximum]
            available = [int(e.get()) for e in self.entries_available]
        except:
            messagebox.showerror("Error", "All fields must be filled with valid integers.")
            return

        need = [[maximum[i][j] - allocation[i][j] for j in range(self.num_resources)] for i in range(self.num_processes)]
        finish = [False] * self.num_processes
        safe_sequence = []
        work = available[:]
        self.canvas.delete("all")
        self.status_text.delete("1.0", tk.END)
        self.process_boxes.clear()

        x, y = 40, 40
        for i in range(self.num_processes):
            box = self.canvas.create_rectangle(x, y, x+180, y+130, fill="#e0e0e0")
            text = self.canvas.create_text(x+90, y+65, text=f"P{i}\nAlloc: {allocation[i]}\nNeed: {need[i]}", font=("Arial", 9))
            self.process_boxes.append((box, text))
            x += 200

        time.sleep(1)
        step = 0
        while step < self.num_processes:
            allocated = False
            for i in range(self.num_processes):
                if not finish[i]:
                    self.canvas.itemconfig(self.process_boxes[i][0], fill="#FFF176")
                    self.status_text.insert(tk.END, f"\n🔍 Checking P{i}...\n")
                    self.status_text.insert(tk.END, f"   Need: {need[i]}\n   Available: {work}\n")

                    if all(need[i][j] <= work[j] for j in range(self.num_resources)):
                        self.status_text.insert(tk.END, f"✅ P{i} can execute.\n")
                        self.canvas.itemconfig(self.process_boxes[i][0], fill="#81C784")
                        self.canvas.itemconfig(self.process_boxes[i][1], text=f"P{i}\n✓ Done")
                        self.canvas.update()
                        time.sleep(1)

                        for j in range(self.num_resources):
                            work[j] += allocation[i][j]

                        finish[i] = True
                        safe_sequence.append(f"P{i}")
                        self.update_available_display(work)
                        allocated = True
                        step += 1
                        break
                    else:
                        for j in range(self.num_resources):
                            if need[i][j] > work[j]:
                                self.status_text.insert(tk.END, f"❌ Cannot allocate R{j}: Need {need[i][j]}, Available {work[j]}\n")
                        self.canvas.itemconfig(self.process_boxes[i][0], fill="#EF5350")
                        self.canvas.itemconfig(self.process_boxes[i][1], text=f"P{i}\nBlocked")
                        self.canvas.update()
                        time.sleep(1)
                        self.canvas.itemconfig(self.process_boxes[i][0], fill="#e0e0e0")
                        self.canvas.itemconfig(self.process_boxes[i][1], text=f"P{i}\nAlloc: {allocation[i]}\nNeed: {need[i]}")

            if not allocated:
                break

        if len(safe_sequence) == self.num_processes:
            self.result_label.config(text="✅ SAFE STATE! Sequence: " + " → ".join(safe_sequence), fg="green")
        else:
            self.result_label.config(text="❌ NOT SAFE! System is in DEADLOCK", fg="red")

    def update_available_display(self, available):
        self.available_label.config(text=f"📦 Available Resources: {available}", fg="blue")
        self.available_label.update()
        time.sleep(1)

# Run the app
root = tk.Tk()
app = ProMaxBankersVisualizerScrollable(root)
root.mainloop()