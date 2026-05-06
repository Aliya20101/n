import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.data = []
        self.load_data()

        # Поля ввода
        self.create_widgets()

    def create_widgets(self):
        # Дата
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Температура
        tk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        # Описание
        tk.Label(self.root, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        # Осадки
        tk.Label(self.root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.StringVar(value="нет")
        tk.Radiobutton(self.root, text="Да", variable=self.precip_var, value="да").grid(row=3, column=1)
        tk.Radiobutton(self.root, text="Нет", variable=self.precip_var, value="нет").grid(row=3, column=2)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=3, pady=10)

        # Таблица записей
        self.tree = ttk.Treeview(self.root, columns=("date", "temp", "desc", "precip"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Фильтрация по дате
        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Фильтровать по дате", command=self.filter_by_date).grid(row=6, column=2, padx=5, pady=5)

        # Фильтрация по температуре
        tk.Label(self.root, text="Фильтр по температуре (>°C):").grid(row=7, column=0, padx=5, pady=5)
        self.filter_temp = tk.Entry(self.root)
        self.filter_temp.grid(row=7, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Фильтровать по температуре", command=self.filter_by_temp).grid(row=7, column=2, padx=5, pady=5)

    def add_record(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precip_var.get()

        if not date or not temp or not desc:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            temp = float(temp)
            if not desc.strip():
                raise ValueError("Описание не может быть пустым.")
            record = {"date": date, "temp": temp, "desc": desc, "precip": precip}
            self.data.append(record)
            self.save_data()
            self.update_tree()
            self.clear_entries()
            messagebox.showinfo("Успех", "Запись добавлена!")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for record in self.data:
            self.tree.insert("", "end", values=(record["date"], record["temp"], record["desc"], record["precip"]))

    def filter_by_date(self):
        date = self.filter_date.get()
        if not date:
            self.update_tree()
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
            filtered = [r for r in self.data if r["date"] == date]
            self.update_tree(filtered)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты!")

    def filter_by_temp(self):
        try:
            temp = float(self.filter_temp.get())
            filtered = [r for r in self.data if r["temp"] > temp]
            self.update_tree(filtered)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат температуры!")

    def update_tree(self, data=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for record in (data or self.data):
            self.tree.insert("", "end", values=(record["date"], record["temp"], record["desc"], record["precip"]))

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
                self.update_tree()
                return True
        except FileNotFoundError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()