import time
import tkinter as tk
from tkinter import ttk


class Stopwatch:
    BACKGROUND = "#081426"
    CARD = "#10213B"
    BLUE = "#3182F6"
    BLUE_HOVER = "#4B93FF"
    TEXT = "#F4F8FF"
    MUTED = "#91A4C1"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Blue Stopwatch")
        self.root.geometry("420x560")
        self.root.minsize(360, 500)
        self.root.configure(bg=self.BACKGROUND)

        self.running = False
        self.started_at = 0.0
        self.elapsed = 0.0
        self.last_lap = 0.0
        self.lap_count = 0

        self._configure_styles()
        self._build_ui()
        self._refresh_display()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Blue.Vertical.TScrollbar",
            background=self.CARD,
            troughcolor=self.CARD,
            bordercolor=self.CARD,
            arrowcolor=self.MUTED,
        )

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, bg=self.BACKGROUND, padx=28, pady=24)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="STOPWATCH",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            container,
            text="Keep your pace.",
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w", pady=(3, 22))

        clock = tk.Frame(container, bg=self.CARD, padx=18, pady=30)
        clock.pack(fill="x")

        self.status_label = tk.Label(
            clock,
            text="●  READY",
            bg=self.CARD,
            fg=self.BLUE,
            font=("Segoe UI", 9, "bold"),
        )
        self.status_label.pack()

        self.time_label = tk.Label(
            clock,
            text="00:00:00.00",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 31, "bold"),
        )
        self.time_label.pack(pady=(14, 0))

        controls = tk.Frame(container, bg=self.BACKGROUND)
        controls.pack(fill="x", pady=22)

        self.start_button = tk.Button(
            controls,
            text="Start",
            command=self.toggle,
            bg=self.BLUE,
            fg="white",
            activebackground=self.BLUE_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            pady=12,
        )
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._add_hover(self.start_button, self.BLUE, self.BLUE_HOVER)

        self.lap_button = tk.Button(
            controls,
            text="Lap",
            command=self.add_lap,
            bg="#1A3152",
            fg=self.TEXT,
            activebackground="#24436D",
            activeforeground=self.TEXT,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            pady=12,
            state="disabled",
        )
        self.lap_button.pack(side="left", fill="x", expand=True, padx=8)
        self._add_hover(self.lap_button, "#1A3152", "#24436D")

        self.reset_button = tk.Button(
            controls,
            text="Reset",
            command=self.reset,
            bg="#1A3152",
            fg=self.TEXT,
            activebackground="#24436D",
            activeforeground=self.TEXT,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            pady=12,
        )
        self.reset_button.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self._add_hover(self.reset_button, "#1A3152", "#24436D")

        lap_header = tk.Frame(container, bg=self.BACKGROUND)
        lap_header.pack(fill="x", pady=(5, 10))
        tk.Label(
            lap_header,
            text="LAPS",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")
        self.lap_count_label = tk.Label(
            lap_header,
            text="0 recorded",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9),
        )
        self.lap_count_label.pack(side="right")

        lap_panel = tk.Frame(container, bg=self.CARD)
        lap_panel.pack(fill="both", expand=True)
        self.lap_list = tk.Listbox(
            lap_panel,
            bg=self.CARD,
            fg=self.TEXT,
            selectbackground="#1A3152",
            selectforeground=self.TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            activestyle="none",
        )
        self.lap_list.pack(fill="both", expand=True, padx=14, pady=8)

    @staticmethod
    def _add_hover(button: tk.Button, normal: str, hover: str) -> None:
        button.bind("<Enter>", lambda event: event.widget.configure(bg=hover))
        button.bind("<Leave>", lambda event: event.widget.configure(bg=normal))

    @staticmethod
    def _format_time(seconds: float) -> str:
        centiseconds = int(seconds * 100)
        hours, remainder = divmod(centiseconds, 360_000)
        minutes, remainder = divmod(remainder, 6_000)
        whole_seconds, centiseconds = divmod(remainder, 100)
        return f"{hours:02}:{minutes:02}:{whole_seconds:02}.{centiseconds:02}"

    def _current_elapsed(self) -> float:
        if self.running:
            return self.elapsed + time.perf_counter() - self.started_at
        return self.elapsed

    def _refresh_display(self) -> None:
        self.time_label.configure(text=self._format_time(self._current_elapsed()))
        self.root.after(10, self._refresh_display)

    def toggle(self) -> None:
        if self.running:
            self.elapsed = self._current_elapsed()
            self.running = False
            self.start_button.configure(text="Resume")
            self.status_label.configure(text="●  PAUSED", fg=self.MUTED)
        else:
            self.started_at = time.perf_counter()
            self.running = True
            self.start_button.configure(text="Pause")
            self.status_label.configure(text="●  RUNNING", fg=self.BLUE)
        self.lap_button.configure(state="normal" if self.running else "disabled")

    def add_lap(self) -> None:
        if not self.running:
            return
        current = self._current_elapsed()
        lap_time = current - self.last_lap
        self.last_lap = current
        self.lap_count += 1
        self.lap_list.insert(
            0,
            f"  LAP {self.lap_count:02}      {self._format_time(lap_time)}"
            f"      TOTAL  {self._format_time(current)}",
        )
        self.lap_count_label.configure(
            text=f"{self.lap_count} recorded" if self.lap_count != 1 else "1 recorded"
        )

    def reset(self) -> None:
        self.running = False
        self.started_at = 0.0
        self.elapsed = 0.0
        self.last_lap = 0.0
        self.lap_count = 0
        self.start_button.configure(text="Start")
        self.status_label.configure(text="●  READY", fg=self.BLUE)
        self.lap_button.configure(state="disabled")
        self.lap_list.delete(0, tk.END)
        self.lap_count_label.configure(text="0 recorded")
        self.time_label.configure(text=self._format_time(0.0))


def main() -> None:
    root = tk.Tk()
    Stopwatch(root)
    root.mainloop()


if __name__ == "__main__":
    main()