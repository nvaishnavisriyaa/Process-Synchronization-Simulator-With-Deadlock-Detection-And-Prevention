import tkinter as tk
from tkinter import messagebox
import threading

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

class ResourceAllocationGraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Resource Allocation Graph (RAG) - Deadlock Detection")

        self.scroll_frame = ScrollableFrame(master)
        self.scroll_frame.pack(fill="both", expand=True)

        self.num_processes = 0
        self.num_resources = 0
        self.process_request_entries = []
        self.resource_allocation_entries = []

        self.setup_ui()

    def setup_ui(self):
        frame = self.scroll_frame.scrollable_frame

        tk.Label(frame, text="No. of Processes:", font=("Arial", 12)).grid(row=0, column=0)
        self.proc_entry = tk.Entry(frame, width=5)
        self.proc_entry.grid(row=0, column=1)

        tk.Label(frame, text="No. of Resources:", font=("Arial", 12)).grid(row=0, column=2)
        self.res_entry = tk.Entry(frame, width=5)
        self.res_entry.grid(row=0, column=3)

        tk.Button(frame, text="Create Inputs", command=self.create_inputs, bg="#4CAF50", fg="white").grid(row=0, column=4)

        self.canvas = tk.Canvas(frame, width=1200, height=600, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas.grid(row=1, column=0, columnspan=10, pady=20)

        self.status_text = tk.Text(frame, height=10, width=150, font=("Consolas", 10))
        self.status_text.grid(row=2, column=0, columnspan=10, pady=10)

        self.result_label = tk.Label(frame, text="", font=("Arial", 16, "bold"))
        self.result_label.grid(row=3, column=0, columnspan=10, pady=10)

    def create_inputs(self):
        frame = self.scroll_frame.scrollable_frame
        try:
            self.num_processes = int(self.proc_entry.get())
            self.num_resources = int(self.res_entry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter valid integers.")
            return

        for widget in frame.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Button):
                widget.destroy()

        self.setup_ui()

        tk.Label(frame, text="Process ➔ Resource (Request)", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=5)
        self.process_request_entries = []
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                e = tk.Entry(frame, width=4)
                e.grid(row=5+i, column=j)
                row.append(e)
            self.process_request_entries.append(row)

        tk.Label(frame, text="Resource ➔ Process (Allocation)", font=("Arial", 10, "bold")).grid(row=4, column=6, columnspan=5)
        self.resource_allocation_entries = []
        for i in range(self.num_resources):
            row = []
            for j in range(self.num_processes):
                e = tk.Entry(frame, width=4)
                e.grid(row=5+self.num_processes+i, column=j)
                row.append(e)
            self.resource_allocation_entries.append(row)

        tk.Button(frame, text="Detect Deadlock", command=self.start_visualization, bg="#2196F3", fg="white").grid(row=6+self.num_processes+self.num_resources, column=0, columnspan=5)

    def start_visualization(self):
        threading.Thread(target=self.visualize).start()

    def visualize(self):
        self.status_text.delete("1.0", tk.END)
        self.canvas.delete("all")

        nodes = [f"P{i}" for i in range(self.num_processes)] + [f"R{j}" for j in range(self.num_resources)]
        graph = {node: [] for node in nodes}

        try:
            for i in range(self.num_processes):
                for j in range(self.num_resources):
                    if self.process_request_entries[i][j].get().strip() == "1":
                        graph[f"P{i}"].append(f"R{j}")
            for i in range(self.num_resources):
                for j in range(self.num_processes):
                    if self.resource_allocation_entries[i][j].get().strip() == "1":
                        graph[f"R{i}"].append(f"P{j}")
        except:
            messagebox.showerror("Invalid Input", "Fill only 0 or 1.")
            return

        pos = {}
        spacing_y = 120

        for idx, node in enumerate(nodes):
            x = 150 if "P" in node else 600
            y = 100 + idx * spacing_y // 2
            pos[node] = (x, y)
            if "P" in node:
                self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#FFD54F")
            else:
                self.canvas.create_rectangle(x-20, y-20, x+20, y+20, fill="#90CAF9")
            self.canvas.create_text(x, y, text=node)

        for src, dests in graph.items():
            for dest in dests:
                x1, y1 = pos[src]
                x2, y2 = pos[dest]
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

        cycle = self.detect_cycle(graph)
        if cycle:
            self.result_label.config(text="❌ Deadlock Detected!\nCycle: " + " → ".join(cycle), fg="red")
        else:
            self.result_label.config(text="✅ No Deadlock. Safe System!", fg="green")

    def detect_cycle(self, graph):
        visited = set()
        rec_stack = set()

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    res = dfs(neighbor, path)
                    if res:
                        return res
                elif neighbor in rec_stack:
                    cycle_idx = path.index(neighbor)
                    return path[cycle_idx:]

            rec_stack.remove(node)
            path.pop()
            return None

        for node in graph:
            if node not in visited:
                path = []
                result = dfs(node, path)
                if result:
                    return result
        return None

# Run app
root = tk.Tk()
app = ResourceAllocationGraphApp(root)
root.mainloop()
