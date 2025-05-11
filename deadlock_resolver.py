import tkinter as tk
from tkinter import ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DeadlockResolverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Deadlock Resolver")
        self.geometry("1100x650")
        self.configure(bg="#f2f2f2")

        self.events = []
        self.processes = {}  # Starts empty

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="🛡️ Deadlock Resolver", font=("Arial", 24, "bold"), bg="#4b79a1", fg="black", pady=10)
        title.pack(fill=tk.X)

        main_frame = tk.Frame(self, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left - Process Controls
        self.left_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.left_frame, text="🧠 Deadlock Resolution", font=("Arial", 16, "bold"), bg="#ffffff", fg="black").pack(pady=10)

        input_frame = tk.Frame(self.left_frame, bg="#ffffff")
        input_frame.pack(pady=(0, 10))

        tk.Label(input_frame, text="Process ID:", bg="#ffffff").grid(row=0, column=0, sticky="e")
        self.pid_entry = tk.Entry(input_frame)
        self.pid_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Resources (comma-separated):", bg="#ffffff").grid(row=1, column=0, sticky="e")
        self.res_entry = tk.Entry(input_frame)
        self.res_entry.grid(row=1, column=1)

        tk.Button(input_frame, text="➕ Add Process", command=self._add_process, bg="#5cb85c", fg="black").grid(row=2, column=0, columnspan=2, pady=5)

        self._render_processes()

        # Right - Timeline and Chart
        self.right_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.right_frame, text="📊 Timeline Tracker", font=("Arial", 16, "bold"), bg="#ffffff", fg="black").pack(pady=10)

        self.event_listbox = tk.Listbox(self.right_frame, font=("Arial", 12), bg="#f9f9f9", fg="black", bd=0, highlightthickness=0)
        self.event_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self._setup_chart()

    def _render_processes(self):
        # Clear old process widgets (except the static label/input)
        for widget in self.left_frame.winfo_children()[2:]:
            widget.destroy()

        for pid, proc in self.processes.items():
            frame = tk.Frame(self.left_frame, bg="#f0f0f0", bd=1, relief=tk.RIDGE, padx=10, pady=5)
            frame.pack(fill=tk.X, pady=6, padx=10)

            info = f"{pid} | Resources: {', '.join(proc['resources'])} | Status: {proc['status']}"
            tk.Label(frame, text=info, font=("Arial", 12), bg="#f0f0f0", fg="black").pack(anchor="w", pady=2)

            if proc["status"] == "running":
                btn_frame = tk.Frame(frame, bg="#f0f0f0")
                btn_frame.pack(anchor="w", pady=2)

                tk.Button(btn_frame, text="❌ Kill", command=lambda p=pid: self.kill_process(p),
                          bg="#d9534f", fg="black", font=("Arial", 10, "bold"),
                          relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)

                for rid in proc["resources"]:
                    tk.Button(btn_frame, text=f"⚡ Preempt {rid}", command=lambda r=rid: self.preempt_resource(r),
                              bg="#f0ad4e", fg="black", font=("Arial", 10),
                              relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)

    def _add_process(self):
        pid = self.pid_entry.get().strip()
        resources = [r.strip() for r in self.res_entry.get().split(",") if r.strip()]

        if pid and resources:
            self.processes[pid] = {"resources": resources, "status": "running"}
            self._log_event(f"🟢 {pid} added with resources {', '.join(resources)}")
            self._render_processes()
            self.pid_entry.delete(0, tk.END)
            self.res_entry.delete(0, tk.END)

    def kill_process(self, pid):
        self.processes[pid]["status"] = "killed"
        self._log_event(f"🔴 {pid} killed")
        self._render_processes()

    def preempt_resource(self, rid):
        self._log_event(f"⚡ Resource {rid} preempted")

    def _log_event(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.append((timestamp, message))
        self.event_listbox.insert(tk.END, f"⏰ {timestamp} — {message}")
        self._update_chart()

    def _setup_chart(self):
        self.figure = Figure(figsize=(5.5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("📈 Event Timeline")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Event Count")
        self.ax.grid(True, linestyle="--", color="gray", alpha=0.6)

        self.canvas = FigureCanvasTkAgg(self.figure, self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

    def _update_chart(self):
        self.ax.clear()
        times = [t for t, _ in self.events]
        y_vals = list(range(1, len(times) + 1))
        self.ax.plot(times, y_vals, marker='o', linestyle='-', color='purple')
        self.ax.set_title("📈 Event Timeline")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Event Count")
        self.ax.grid(True, linestyle="--", color="gray", alpha=0.6)
        self.figure.autofmt_xdate()
        self.canvas.draw()


if __name__ == "__main__":
    app = DeadlockResolverApp()
    app.mainloop()
