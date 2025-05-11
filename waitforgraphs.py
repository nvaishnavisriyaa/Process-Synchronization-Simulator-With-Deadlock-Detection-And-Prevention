import tkinter as tk
from tkinter import messagebox
import math

class WaitForGraphVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Deadlock Visualizer - Clear Output Below")

        self.processes = []
        self.resources = []
        self.held_resources = {}
        self.requested_resources = {}
        self.edges = []
        self.cycle_nodes = set()
        self.cycle_path = []

        # Compact canvas
        self.canvas = tk.Canvas(master, width=900, height=600, bg="white", scrollregion=(0, 0, 900, 600))
        self.canvas.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky="nsew")

        self.v_scroll = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=2, sticky="ns")
        self.h_scroll = tk.Scrollbar(master, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=1, sticky="ew")

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Controls on left
        self.controls_frame = tk.Frame(master)
        self.controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        tk.Label(self.controls_frame, text="Processes (comma-separated):").grid(row=0, column=0, sticky="w")
        self.proc_entry = tk.Entry(self.controls_frame, width=30)
        self.proc_entry.grid(row=0, column=1)

        tk.Label(self.controls_frame, text="Resources (comma-separated):").grid(row=1, column=0, sticky="w")
        self.res_entry = tk.Entry(self.controls_frame, width=30)
        self.res_entry.grid(row=1, column=1)

        tk.Label(self.controls_frame, text="Held (P:R, e.g. P1:R1,P2:R2):").grid(row=2, column=0, sticky="w")
        self.held_entry = tk.Entry(self.controls_frame, width=30)
        self.held_entry.grid(row=2, column=1)

        tk.Label(self.controls_frame, text="Requested (P:R, e.g. P1:R2,P2:R1):").grid(row=3, column=0, sticky="w")
        self.req_entry = tk.Entry(self.controls_frame, width=30)
        self.req_entry.grid(row=3, column=1)

        tk.Button(self.controls_frame, text="Visualize", command=self.setup_graph, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=5)

        # Output below all
        self.output_box = tk.Text(master, height=10, width=150, wrap=tk.WORD)
        self.output_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    def setup_graph(self):
        self.canvas.delete("all")
        self.output_box.delete("1.0", tk.END)
        self.cycle_nodes.clear()
        self.cycle_path = []

        try:
            self.processes = [p.strip() for p in self.proc_entry.get().split(",")]
            self.resources = [r.strip() for r in self.res_entry.get().split(",")]

            held_pairs = [pair.strip() for pair in self.held_entry.get().split(",")]
            self.held_resources = {p.split(":")[0]: p.split(":")[1] for p in held_pairs}

            req_pairs = [pair.strip() for pair in self.req_entry.get().split(",")]
            self.requested_resources = {p.split(":")[0]: p.split(":")[1] for p in req_pairs}

        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input format. Error: {e}")
            return

        self.edges = []
        for p in self.processes:
            held = self.held_resources.get(p)
            requested = self.requested_resources.get(p)

            if held and requested:
                for other_p, other_held in self.held_resources.items():
                    if other_held == requested:
                        self.edges.append((p, other_p))
                        self.output_box.insert(tk.END, f"🔍 {p} holds {held}, requests {requested} → waiting for {other_p}\n")

        has_cycle = self.detect_cycle()
        self.draw_graph()

        if has_cycle:
            cycle_str = " → ".join(self.cycle_path + [self.cycle_path[0]])
            self.output_box.insert(tk.END, f"\n❌ Deadlock Detected! Cycle: {cycle_str}\n")
        else:
            self.output_box.insert(tk.END, "\n✅ No Deadlock. System is safe.\n")

    def draw_graph(self):
        positions = {}
        radius = 30
        center_x, center_y = 450, 300
        angle_step = 360 / len(self.processes) if self.processes else 1

        for i, p in enumerate(self.processes):
            angle = math.radians(i * angle_step)
            x = center_x + 200 * math.cos(angle)
            y = center_y + 200 * math.sin(angle)
            positions[p] = (x, y)
            node_color = "#FFD54F" if p not in self.cycle_nodes else "#FF6F61"
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=node_color, outline="black", width=2)
            self.canvas.create_text(x, y, text=p, font=("Arial", 12, "bold"))

        for (src, dst) in self.edges:
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            edge_color = "red" if src in self.cycle_nodes and dst in self.cycle_nodes else "green"
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=3, fill=edge_color)

    def detect_cycle(self):
        graph = {p: [] for p in self.processes}
        for src, dst in self.edges:
            graph[src].append(dst)

        visited = set()
        rec_stack = set()

        def dfs(v, path):
            visited.add(v)
            rec_stack.add(v)
            path.append(v)
            for neighbor in graph.get(v, []):
                if neighbor not in visited:
                    if dfs(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    self.cycle_nodes.update(path)
                    self.cycle_path = path[path.index(neighbor):]
                    return True
            rec_stack.remove(v)
            path.pop()
            return False

        for node in self.processes:
            if node not in visited:
                if dfs(node, []):
                    return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1500x900")
    app = WaitForGraphVisualizer(root)
    root.mainloop()