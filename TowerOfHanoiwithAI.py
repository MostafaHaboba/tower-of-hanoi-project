import tkinter as tk
from tkinter import messagebox, font


class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.reset_game()

    def move_disk(self, source=None, target=None, manual=True):
        if manual:
            try:
                source = int(self.source_entry.get())
                target = int(self.target_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid tower numbers.")
                return

        if source == target:
            self.status_label.config(text="Invalid move: Same tower!")
            return
        if not self.towers[source]:
            self.status_label.config(text="Invalid move: Source tower is empty!")
            return
        if self.towers[target] and self.towers[source][-1] > self.towers[target][-1]:
            self.status_label.config(text="Invalid move: Larger disk on smaller one.")
            return

        disk = self.towers[source].pop()
        self.towers[target].append(disk)
        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")
        self.status_label.config(text=f"Moved disk {disk} from Tower {source} to Tower {target}")
        self.draw_towers()

    def reset_game(self):
        self.towers = [[3, 2, 1], [], []]
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.status_label.config(text="")
        self.draw_towers()

    def draw_towers(self):
        self.canvas.delete("all")
        base_y = 350
        tower_width = 10
        for i, tower in enumerate(self.towers):
            x_center = 100 + i * 150
            self.canvas.create_line(x_center, base_y - 100, x_center, base_y, fill="black", width=4)
            for j, disk in enumerate(tower):
                self.canvas.create_rectangle(x_center - disk * 15, base_y - (j + 1) * 20, x_center + disk * 15,
                                             base_y - j * 20, fill="blue", outline="grey")

    def setup_gui(self):
        self.root.title("Tower of Hanoi")
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='white')
        self.canvas.pack(pady=20)

        custom_font = font.Font(family='Helvetica', size=12, weight='bold')
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, ipadx=5, ipady=5)

        tk.Label(control_frame, text="Source Tower (0-2):", font=custom_font).grid(row=0, column=0)
        self.source_entry = tk.Entry(control_frame, width=5, font=custom_font)
        self.source_entry.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Target Tower (0-2):", font=custom_font).grid(row=0, column=2)
        self.target_entry = tk.Entry(control_frame, width=5, font=custom_font)
        self.target_entry.grid(row=0, column=3, padx=5)

        tk.Button(control_frame, text="Move Disk", command=self.move_disk, font=custom_font, relief=tk.RAISED,
                  bg='lightblue').grid(row=1, column=0, columnspan=2, pady=5)
        tk.Button(control_frame, text="Reset Game", command=self.reset_game, font=custom_font, relief=tk.RAISED,
                  bg='lightgreen').grid(row=1, column=2, columnspan=2)

        tk.Button(control_frame, text="Solve with AI", command=self.solve_game_with_ai, font=custom_font,
                  relief=tk.RAISED, bg='lightcoral').grid(row=2, column=1, columnspan=2, pady=5)

        self.moves_label = tk.Label(self.root, text="Moves: 0", font=custom_font)
        self.moves_label.pack()

        self.status_label = tk.Label(self.root, text="", font=custom_font)
        self.status_label.pack()

    def solve_game_with_ai(self):
        self.n = 3  # number of disks
        self.reset_game()
        self.solve_tower_of_hanoi(self.n, 0, 2, 1)

    def solve_tower_of_hanoi(self, n, source, target, auxiliary, delay=500):
        if n == 1:
            self.root.after(delay, self.move_disk, source, target, False)
        else:
            self.solve_tower_of_hanoi(n - 1, source, auxiliary, target, delay)
            self.root.after(delay * (2 ** n - 1), self.move_disk, source, target, False)
            self.solve_tower_of_hanoi(n - 1, auxiliary, target, source, delay + delay * (2 ** n))


if __name__ == "__main__":
    root = tk.Tk()
    game = TowerOfHanoi(root)
    root.mainloop()
