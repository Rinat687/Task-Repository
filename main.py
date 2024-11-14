import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime


# Функция для добавления задачи
def add_task():
    task = task_entry.get()  # Получаем текст из поля ввода
    if task:
        priority = priority_entry.get()  # Получаем приоритет из поля ввода
        if not priority:
            priority = "Низкий"  # Устанавливаем низкий приоритет по умолчанию
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущую дату и время
        task_listBox.insert(tk.END,
                            f"{task} | Приоритет: {priority} | Создано: {timestamp}")  # Вставляем задачу в список
        task_entry.delete(0, tk.END)  # Очищаем поле для ввода
        priority_entry.delete(0, tk.END)  # Очищаем поле для ввода приоритета

        # Добавляем задачу в файл
        with open("tasks.txt", "a", encoding="utf-8") as file:
            file.write(f"{task} | Приоритет: {priority} | Создано: {timestamp}\n")  # Записываем задачу


# Функция для удаления задачи
def delete_task():
    selected_task = task_listBox.curselection()  # Получаем индекс выбранной задачи
    if selected_task:
        task_listBox.delete(selected_task)  # Удаляем задачу из списка

        # Читаем все задачи из файла
        with open("tasks.txt", "r", encoding="utf-8") as file:
            tasks = file.readlines()  # Читаем все строки из файла

        # Удаляем задачу из списка задач
        tasks.pop(selected_task[0])  # Удаляем задачу по индексу

        # Записываем обновленный список задач обратно в файл
        with open("tasks.txt", "w", encoding="utf-8") as file:
            file.writelines(tasks)  # Записываем оставшиеся задачи в файл


# Функция для отметки задачи как выполненной
def mark_task():
    selected_task = task_listBox.curselection()  # Получаем индекс выбранной задачи

    if selected_task:
        task_index = selected_task[0]  # Получаем индекс первой выбранной задачи
        task_to_mark = task_listBox.get(selected_task)  # Получаем текст задачи для отметки

        updated_task = f"[Выполнено] {task_to_mark.strip()}\n"  # Добавляем метку к выполненной задаче

        # Обновляем задачу в списке
        task_listBox.itemconfig(task_index, bg="slate blue")

        tasks = load_tasks_from_file()

        if task_index < len(tasks):
            tasks[task_index] = updated_task

            with open("tasks.txt", "w", encoding="utf-8") as file:
                file.writelines(tasks)  # Записываем оставшиеся задачи в файл


# Функция для загрузки задач из файла
def load_tasks():
    """Загружает задачи из файла и добавляет их в список."""
    try:
        tasks = load_tasks_from_file()

        for task in tasks:
            task_listBox.insert(tk.END, task.strip())  # Добавляем задачу в список без символа новой строки

            if "[Выполнено]" in task:  # Если задача выполнена, меняем цвет фона
                index = task_listBox.size() - 1
                task_listBox.itemconfig(index, bg="slate blue")

    except FileNotFoundError:
        pass  # Если файл не найден, просто пропускаем


def load_tasks_from_file():
    """Читает задачи из файла и возвращает их в виде списка."""
    with open("tasks.txt", "r", encoding="utf-8") as file:
        return file.readlines()


# Функция для редактирования выбранной задачи
def edit_task():
    selected_task = task_listBox.curselection()  # Получаем индекс выбранной задачи

    if selected_task:
        index = selected_task[0]
        current_task = task_listBox.get(selected_task)

        new_task = simpledialog.askstring("Редактировать задачу", "Введите новую задачу:",
                                          initialvalue=current_task.split('|')[0].strip())

        if new_task is not None:
            priority = simpledialog.askstring("Приоритет", "Введите приоритет (высокий/средний/низкий):",
                                              initialvalue=current_task.split('|')[1].strip())
            if not priority:
                priority = "Низкий"  # Устанавливаем низкий приоритет по умолчанию

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Обновляем дату создания

            updated_task = f"{new_task} | Приоритет: {priority} | Создано: {timestamp}\n"

            task_listBox.delete(index)  # Удаляем старую задачу из списка
            task_listBox.insert(index, updated_task)  # Вставляем обновленную задачу

            tasks = load_tasks_from_file()
            tasks[index] = updated_task

            with open("tasks.txt", "w", encoding="utf-8") as file:
                file.writelines(tasks)  # Записываем оставшиеся задачи в файл


# Функция для сортировки задач по алфавиту
def sort_tasks():
    tasks = load_tasks_from_file()
    tasks.sort(key=lambda x: x.split('|')[0])  # Сортируем по тексту задачи

    with open("tasks.txt", "w", encoding="utf-8") as file:
        file.writelines(tasks)  # Записываем отсортированные задачи обратно в файл

    load_tasks()  # Перезагружаем список задач


# Функция для поиска задач
def search_tasks():
    search_term = simpledialog.askstring("Поиск задач", "Введите текст для поиска:")

    if search_term is not None and search_term.strip():
        results = []

        for index in range(task_listBox.size()):
            task_text = task_listBox.get(index)
            if search_term.lower() in task_text.lower():  # Игнорируем регистр
                results.append(task_text)

        # Очищаем текущий список задач перед показом результатов поиска
        task_listBox.delete(0, tk.END)

        if results:
            for result in results:
                task_listBox.insert(tk.END, result)  # Показываем найденные задачи

            messagebox.showinfo("Результат поиска", f"Найдены следующие задачи:\n" + "\n".join(results))

        else:
            messagebox.showinfo("Результат поиска", "Задача не найдена.")
            load_tasks()  # Загружаем все задачи обратно, если ничего не найдено


# Создаем основное окно
root = tk.Tk()
root.title("Your Tasks!")
root.geometry("400x600")
root.configure(background="medium purple")

# Создаем метку для ввода задачи
label1 = tk.Label(root, text="Введите вашу задачу:", bg="medium purple", fg="grey30", font=("Arial", 14))
label1.pack(pady=5)

# Создаем поле для ввода задачи
task_entry = tk.Entry(root, width=40, bg="purple1")
task_entry.pack(pady=5)

# Создаем метку для ввода приоритета
label2 = tk.Label(root, text="Введите приоритет (высокий/средний/низкий):", bg="medium purple", fg="grey30",
                  font=("Arial", 14))
label2.pack(pady=5)

# Создаем поле для ввода приоритета
priority_entry = tk.Entry(root, width=40, bg="purple1")
priority_entry.pack(pady=5)

# Создаем кнопку добавления задачи
add_task_button = tk.Button(root, text="Добавить задачу", bg="purple4", fg="grey100", width=25, command=add_task)
add_task_button.pack(pady=5)

# Создаем кнопку удаления задачи
delete_button = tk.Button(root, text="Удалить задачу", bg="purple4", fg="grey100", width=25, command=delete_task)
delete_button.pack(pady=5)

# Создаем кнопку отметки выполненной задачи
mark_button = tk.Button(root, text="Отметить выполненную задачу", bg="purple4", fg="grey100", width=25,
                        command=mark_task)
mark_button.pack(pady=5)

# Создаем кнопку редактирования задачи
edit_button = tk.Button(root, text="Редактировать задачу", bg="purple4", fg="grey100", width=25,
                        command=edit_task)
edit_button.pack(pady=5)

# Создаем кнопку сортировки задач
sort_button = tk.Button(root, text="Сортировать задачи по алфавиту", bg="purple4", fg="grey100",
                        command=sort_tasks)
sort_button.pack(pady=5)

# Создаем кнопку поиска задач
search_button = tk.Button(root, text="Поиск задач", bg="purple4", fg="grey100",
                          command=search_tasks)
search_button.pack(pady=5)

# Создаем метку для списка задач
label3 = tk.Label(root, text="Список задач:", bg="medium purple", fg="grey30", font=("Arial", 14))
label3.pack(pady=5)

task_listBox = tk.Listbox(root, height=20, width=50, bg="MediumPurple1")
task_listBox.pack(pady=5)

# Загружаем задачи при запуске программы
load_tasks()
# Запускаем основной цикл приложения
root.mainloop()