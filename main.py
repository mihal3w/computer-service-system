import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import datetime
from tkinter import font as tkfont


clients = []
products = []
categories = {}
sales = []
repairs = []
users = []

def load_clients():
    try:
        with open("КомпСервиз/clients.txt", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    id_, name, phone, email = line.strip().split(";")
                    clients.append({"id": id_, "name": name, "phone": phone, "email": email})
    except FileNotFoundError:
        print("Файлът с клиенти не е намерен. Създава се нов.")
        open("КомпСервиз/clients.txt", "w", encoding="utf-8").close()

def load_products():
    try:
        with open("КомпСервиз/products.txt", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    id_, model, type_, brand, price = line.strip().split(";")
                    products.append({"id": id_, "model": model, "type": type_, "brand": brand, "price": float(price)})
    except FileNotFoundError:
        print("Файлът с продукти не е намерен. Създава се нов.")
        open("КомпСервиз/products.txt", "w", encoding="utf-8").close()

def load_categories():
    try:
        with open("КомпСервиз/categories.txt", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    id_, name = line.strip().split(";")
                    categories[id_] = name
    except FileNotFoundError:
        print("Файлът с категории не е намерен. Създава се нов.")
        open("КомпСервиз/categories.txt", "w", encoding="utf-8").close()

def load_sales():
    try:
        with open("КомпСервиз/sales.txt", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    id_, client_id, product_id, date, price, quantity = line.strip().split(";")
                    sales.append({"id": id_, "client_id": client_id, "product_id": product_id, 
                                 "date": date, "price": float(price), "quantity": int(quantity)})
    except FileNotFoundError:
        print("Файлът с продажби не е намерен. Създава се нов.")
        open("КомпСервиз/sales.txt", "w", encoding="utf-8").close()

def load_repairs():
    try:
        with open("КомпСервиз/repairs.txt", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    id_, client_id, product_id, date, desc, price = line.strip().split(";")
                    repairs.append({"id": id_, "client_id": client_id, "product_id": product_id, 
                                  "date": date, "desc": desc, "price": float(price)})
    except FileNotFoundError:
        print("Файлът с ремонти не е намерен. Създава се нов.")
        open("КомпСервиз/repairs.txt", "w", encoding="utf-8").close()

def load_users():
    try:
        with open("КомпСервиз/admins.txt", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split(";")
                    users.append({"username": username, "password": password})
    except FileNotFoundError:
        print("Файлът с администратори не е намерен. Създава се нов със стандартен акаунт.")
        with open("КомпСервиз/admins.txt", "w", encoding="utf-8") as f:
            f.write("admin;admin\n")
        users.append({"username": "admin", "password": "admin"})

def load_all():

    if not os.path.exists("КомпСервиз"):
        os.makedirs("КомпСервиз")
    
    load_users()
    load_clients()
    load_products()
    load_categories()
    load_sales()
    load_repairs()

def login_screen():
    login_window = tk.Tk()
    login_window.title("Вход в системата")
    login_window.geometry("400x300")
    login_window.resizable(False, False)
    
    
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 12))
    style.configure('TEntry', font=('Arial', 12))
    

    ttk.Label(login_window, text="Компютърен Сервиз", font=('Arial', 16, 'bold')).pack(pady=20)
    

    ttk.Label(login_window, text="Потребителско име:").pack()
    username_entry = ttk.Entry(login_window)
    username_entry.pack(pady=5)
    

    ttk.Label(login_window, text="Парола:").pack()
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if any(user['username'] == username and user['password'] == password for user in users):
            login_window.destroy()
            main_menu()
        else:
            messagebox.showerror("Грешка", "Невалидно потребителско име или парола!")
    
    login_btn = ttk.Button(login_window, text="Вход", command=attempt_login)
    login_btn.pack(pady=20)
    
    login_window.mainloop()


def main_menu():
    root = tk.Tk()
    root.title("Компютърен Сервиз - Главно меню")
    root.geometry("1000x700")
    root.resizable(False, False)
    

    style = ttk.Style()
    style.configure('Header.TLabel', font=('Arial', 20, 'bold'), foreground='#2c3e50')
    style.configure('Date.TLabel', font=('Arial', 12), foreground='#7f8c8d')
    style.configure('Menu.TButton', font=('Arial', 12), padding=10, width=25)
    

    header_frame = ttk.Frame(root)
    header_frame.pack(pady=20)
    
    today = datetime.date.today().strftime("%d.%m.%Y")
    ttk.Label(header_frame, text="Компютърен Сервиз", style='Header.TLabel').pack()
    ttk.Label(header_frame, text=f"Днес е {today}", style='Date.TLabel').pack()
    

    menu_frame = ttk.Frame(root)
    menu_frame.pack(pady=30)
    
    buttons = [
        ("Клиенти", show_clients),
        ("Продукти", show_products),
        ("Ремонти", show_all_repairs),
        ("Продажби", show_sales),
        ("Справки", reports_menu),
        ("Добави клиент", add_client),
        ("Добави продукт", add_product),
        ("Добави ремонт", add_repair),
        ("Касова бележка", generate_receipt),
        ("Изход", lambda: root.destroy())
    ]
    
    for i, (text, command) in enumerate(buttons):
        btn = ttk.Button(menu_frame, text=text, command=command, style='Menu.TButton')
        btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    root.mainloop()


def reports_menu():
    win = tk.Toplevel()
    win.title("Справки")
    win.geometry("400x400")
    
    ttk.Label(win, text="Избери справка:", font=('Arial', 14)).pack(pady=20)
    
    reports = [
        ("Ремонти по клиент", client_repairs),
        ("Продажби по дата", search_sales_by_date),
        ("Филтриране на продукти", filter_products_by_type),
        ("Справка за клиент", client_report),
        ("Обща статистика", show_statistics)
    ]
    
    for text, command in reports:
        ttk.Button(win, text=text, command=command, width=30).pack(pady=5)


def get_client_name(client_id):
    client = next((c for c in clients if c['id'] == client_id), None)
    return client['name'] if client else "Неизвестен"

def get_product_model(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return product['model'] if product else "Неизвестен"

def get_product_price(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return product['price'] if product else 0.0

def generate_id(prefix, items):
    max_id = 0
    for item in items:
        num = int(item['id'].replace(prefix, ''))
        if num > max_id:
            max_id = num
    return f"{prefix}{max_id + 1:03d}"

def save_clients():
    with open("КомпСервиз/clients.txt", "w", encoding="utf-8") as f:
        for c in clients:
            f.write(f"{c['id']};{c['name']};{c['phone']};{c['email']}\n")

def save_products():
    with open("КомпСервиз/products.txt", "w", encoding="utf-8") as f:
        for p in products:
            f.write(f"{p['id']};{p['model']};{p['type']};{p['brand']};{p['price']:.2f}\n")

def save_repairs():
    with open("КомпСервиз/repairs.txt", "w", encoding="utf-8") as f:
        for r in repairs:
            f.write(f"{r['id']};{r['client_id']};{r['product_id']};{r['date']};{r['desc']};{r['price']:.2f}\n")

def save_sales():
    with open("КомпСервиз/sales.txt", "w", encoding="utf-8") as f:
        for s in sales:
            f.write(f"{s['id']};{s['client_id']};{s['product_id']};{s['date']};{s['price']:.2f};{s['quantity']}\n")


def show_clients():
    win = tk.Toplevel()
    win.title("Клиенти")
    win.geometry("800x600")
    

    search_frame = ttk.Frame(win)
    search_frame.pack(pady=10, fill=tk.X)
    
    ttk.Label(search_frame, text="Търсене:").pack(side=tk.LEFT)
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def update_list(event=None):
        search_term = search_entry.get().lower()
        tree.delete(*tree.get_children())
        for c in clients:
            if (search_term in c['id'].lower() or 
                search_term in c['name'].lower() or 
                search_term in c['phone'].lower() or 
                search_term in c['email'].lower()):
                tree.insert("", tk.END, values=(c['id'], c['name'], c['phone'], c['email']))
    
    search_entry.bind("<KeyRelease>", update_list)
    

    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("id", "name", "phone", "email"), show="headings",
                        yscrollcommand=scrollbar.set)
    
    tree.heading("id", text="ID")
    tree.heading("name", text="Име")
    tree.heading("phone", text="Телефон")
    tree.heading("email", text="Имейл")
    
    tree.column("id", width=100)
    tree.column("name", width=200)
    tree.column("phone", width=150)
    tree.column("email", width=250)
    
    for c in clients:
        tree.insert("", tk.END, values=(c['id'], c['name'], c['phone'], c['email']))
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    

    def edit_client():
        selected = tree.focus()
        if not selected:
            return
        client_data = tree.item(selected)['values']
        edit_client_window(client_data[0])
    
    def delete_client():
        selected = tree.focus()
        if not selected:
            return
        client_id = tree.item(selected)['values'][0]
        if messagebox.askyesno("Потвърждение", "Сигурни ли сте, че искате да изтриете клиента?"):
            global clients
            clients = [c for c in clients if c['id'] != client_id]
            save_clients()
            update_list()
    
    menu = tk.Menu(win, tearoff=0)
    menu.add_command(label="Редактирай", command=edit_client)
    menu.add_command(label="Изтрий", command=delete_client)
    
    def show_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.focus(item)
            menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", show_menu)

def edit_client_window(client_id):
    client = next((c for c in clients if c['id'] == client_id), None)
    if not client:
        return
    
    win = tk.Toplevel()
    win.title("Редактиране на клиент")
    
    ttk.Label(win, text="ID:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
    ttk.Label(win, text=client['id']).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
    
    ttk.Label(win, text="Име:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    name_entry = ttk.Entry(win)
    name_entry.insert(0, client['name'])
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Телефон:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
    phone_entry = ttk.Entry(win)
    phone_entry.insert(0, client['phone'])
    phone_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Имейл:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
    email_entry = ttk.Entry(win)
    email_entry.insert(0, client['email'])
    email_entry.grid(row=3, column=1, padx=5, pady=5)
    
    def save_changes():
        client['name'] = name_entry.get()
        client['phone'] = phone_entry.get()
        client['email'] = email_entry.get()
        save_clients()
        messagebox.showinfo("Успех", "Клиентът е обновен успешно!")
        win.destroy()
    
    ttk.Button(win, text="Запази", command=save_changes).grid(row=4, columnspan=2, pady=10)

def add_client():
    win = tk.Toplevel()
    win.title("Добавяне на клиент")
    
    ttk.Label(win, text="Име:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
    name_entry = ttk.Entry(win)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Телефон:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    phone_entry = ttk.Entry(win)
    phone_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Имейл:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
    email_entry = ttk.Entry(win)
    email_entry.grid(row=2, column=1, padx=5, pady=5)
    
    def save_client():
        new_id = generate_id("CL", clients)
        new_client = {
            "id": new_id,
            "name": name_entry.get(),
            "phone": phone_entry.get(),
            "email": email_entry.get()
        }
        clients.append(new_client)
        save_clients()
        messagebox.showinfo("Успех", f"Клиентът е добавен успешно с ID: {new_id}")
        win.destroy()
    
    ttk.Button(win, text="Запази", command=save_client).grid(row=3, columnspan=2, pady=10)

def show_products():
    win = tk.Toplevel()
    win.title("Продукти")
    win.geometry("900x600")
    

    filter_frame = ttk.Frame(win)
    filter_frame.pack(pady=10, fill=tk.X)
    
    ttk.Label(filter_frame, text="Търсене:").pack(side=tk.LEFT)
    search_entry = ttk.Entry(filter_frame)
    search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    ttk.Label(filter_frame, text="Тип:").pack(side=tk.LEFT, padx=(10,0))
    type_combo = ttk.Combobox(filter_frame, values=["Всички"] + sorted(set(p['type'] for p in products)))
    type_combo.pack(side=tk.LEFT)
    type_combo.current(0)
    
    def update_list(event=None):
        search_term = search_entry.get().lower()
        selected_type = type_combo.get()
        
        tree.delete(*tree.get_children())
        for p in products:
            if (search_term in p['id'].lower() or 
                search_term in p['model'].lower() or 
                search_term in p['type'].lower() or 
                search_term in p['brand'].lower()):
                if selected_type == "Всички" or p['type'] == selected_type:
                    tree.insert("", tk.END, values=(p['id'], p['model'], p['type'], p['brand'], f"{p['price']:.2f}"))
    
    search_entry.bind("<KeyRelease>", update_list)
    type_combo.bind("<<ComboboxSelected>>", update_list)
    

    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("id", "model", "type", "brand", "price"), show="headings",
                        yscrollcommand=scrollbar.set)
    
    tree.heading("id", text="ID")
    tree.heading("model", text="Модел")
    tree.heading("type", text="Тип")
    tree.heading("brand", text="Марка")
    tree.heading("price", text="Цена")
    
    tree.column("id", width=100)
    tree.column("model", width=200)
    tree.column("type", width=150)
    tree.column("brand", width=150)
    tree.column("price", width=100)
    
    update_list()
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    

    def edit_product():
        selected = tree.focus()
        if not selected:
            return
        product_id = tree.item(selected)['values'][0]
        edit_product_window(product_id)
    
    def delete_product():
        selected = tree.focus()
        if not selected:
            return
        product_id = tree.item(selected)['values'][0]
        if messagebox.askyesno("Потвърждение", "Сигурни ли сте, че искате да изтриете продукта?"):
            global products
            products = [p for p in products if p['id'] != product_id]
            save_products()
            update_list()
    
    menu = tk.Menu(win, tearoff=0)
    menu.add_command(label="Редактирай", command=edit_product)
    menu.add_command(label="Изтрий", command=delete_product)
    
    def show_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.focus(item)
            menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", show_menu)

def edit_product_window(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return
    
    win = tk.Toplevel()
    win.title("Редактиране на продукт")
    
    ttk.Label(win, text="ID:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
    ttk.Label(win, text=product['id']).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
    
    ttk.Label(win, text="Модел:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    model_entry = ttk.Entry(win)
    model_entry.insert(0, product['model'])
    model_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Тип:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
    type_entry = ttk.Entry(win)
    type_entry.insert(0, product['type'])
    type_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Марка:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
    brand_entry = ttk.Entry(win)
    brand_entry.insert(0, product['brand'])
    brand_entry.grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Цена:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
    price_entry = ttk.Entry(win)
    price_entry.insert(0, str(product['price']))
    price_entry.grid(row=4, column=1, padx=5, pady=5)
    
    def save_changes():
        try:
            product['model'] = model_entry.get()
            product['type'] = type_entry.get()
            product['brand'] = brand_entry.get()
            product['price'] = float(price_entry.get())
            save_products()
            messagebox.showinfo("Успех", "Продуктът е обновен успешно!")
            win.destroy()
        except ValueError:
            messagebox.showerror("Грешка", "Невалидна цена!")
    
    ttk.Button(win, text="Запази", command=save_changes).grid(row=5, columnspan=2, pady=10)

def add_product():
    win = tk.Toplevel()
    win.title("Добавяне на продукт")
    
    ttk.Label(win, text="Модел:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
    model_entry = ttk.Entry(win)
    model_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Тип:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    type_entry = ttk.Entry(win)
    type_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Марка:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
    brand_entry = ttk.Entry(win)
    brand_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(win, text="Цена:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
    price_entry = ttk.Entry(win)
    price_entry.grid(row=3, column=1, padx=5, pady=5)
    
    def save_product():
        try:
            new_id = generate_id("PR", products)
            new_product = {
                "id": new_id,
                "model": model_entry.get(),
                "type": type_entry.get(),
                "brand": brand_entry.get(),
                "price": float(price_entry.get())
            }
            products.append(new_product)
            save_products()
            messagebox.showinfo("Успех", f"Продуктът е добавен успешно с ID: {new_id}")
            win.destroy()
        except ValueError:
            messagebox.showerror("Грешка", "Невалидна цена!")
    
    ttk.Button(win, text="Запази", command=save_product).grid(row=4, columnspan=2, pady=10)

def show_sales():
    win = tk.Toplevel()
    win.title("Всички продажби")
    win.geometry("1000x600")
    

    filter_frame = ttk.Frame(win)
    filter_frame.pack(pady=10, fill=tk.X)
    
    ttk.Label(filter_frame, text="От дата:").pack(side=tk.LEFT)
    date_from = ttk.Entry(filter_frame, width=10)
    date_from.pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="До дата:").pack(side=tk.LEFT, padx=(10,0))
    date_to = ttk.Entry(filter_frame, width=10)
    date_to.pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="Клиент:").pack(side=tk.LEFT, padx=(10,0))
    client_combo = ttk.Combobox(filter_frame, values=["Всички"] + [f"{c['id']} - {c['name']}" for c in clients])
    client_combo.pack(side=tk.LEFT)
    client_combo.current(0)
    
    ttk.Label(filter_frame, text="Продукт:").pack(side=tk.LEFT, padx=(10,0))
    product_combo = ttk.Combobox(filter_frame, values=["Всички"] + [f"{p['id']} - {p['model']}" for p in products])
    product_combo.pack(side=tk.LEFT)
    product_combo.current(0)
    
    def update_list():
        tree.delete(*tree.get_children())
        date_f = date_from.get()
        date_t = date_to.get()
        client = client_combo.get().split(" - ")[0] if client_combo.get() != "Всички" else None
        product = product_combo.get().split(" - ")[0] if product_combo.get() != "Всички" else None
        
        total = 0
        for s in sales:
            if ((not date_f or s['date'] >= date_f) and 
                (not date_t or s['date'] <= date_t) and 
                (not client or s['client_id'] == client) and
                (not product or s['product_id'] == product)):
                
                client_name = get_client_name(s['client_id'])
                product_model = get_product_model(s['product_id'])
                sale_total = s['price'] * s['quantity']
                total += sale_total
                tree.insert("", tk.END, values=(
                    s['id'], s['date'], client_name, product_model, 
                    f"{s['price']:.2f}", s['quantity'], f"{sale_total:.2f}"
                ))
        
        total_label.config(text=f"Общо: {total:.2f} лв")
    
    ttk.Button(filter_frame, text="Филтрирай", command=update_list).pack(side=tk.LEFT, padx=10)
    

    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("id", "date", "client", "product", "price", "quantity", "total"), 
                        show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("id", text="ID")
    tree.heading("date", text="Дата")
    tree.heading("client", text="Клиент")
    tree.heading("product", text="Продукт")
    tree.heading("price", text="Ед. цена")
    tree.heading("quantity", text="Количество")
    tree.heading("total", text="Общо")
    
    tree.column("id", width=80)
    tree.column("date", width=100)
    tree.column("client", width=150)
    tree.column("product", width=150)
    tree.column("price", width=100)
    tree.column("quantity", width=80)
    tree.column("total", width=100)
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    

    total_frame = ttk.Frame(win)
    total_frame.pack(fill=tk.X, pady=5)
    
    total_label = ttk.Label(total_frame, text="Общо: 0.00 лв", font=('Arial', 12, 'bold'))
    total_label.pack(side=tk.RIGHT, padx=10)
    

    def add_sale():
        sale_win = tk.Toplevel()
        sale_win.title("Нова продажба")
        
        ttk.Label(sale_win, text="Клиент:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        client_combo = ttk.Combobox(sale_win, values=[f"{c['id']} - {c['name']}" for c in clients])
        client_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(sale_win, text="Продукт:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        product_combo = ttk.Combobox(sale_win, values=[f"{p['id']} - {p['model']}" for p in products])
        product_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(sale_win, text="Количество:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        quantity_entry = ttk.Entry(sale_win)
        quantity_entry.insert(0, "1")
        quantity_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        def calculate_price():
            product_id = product_combo.get().split(" - ")[0]
            price = get_product_price(product_id)
            quantity = int(quantity_entry.get())
            total_price = price * quantity
            price_label.config(text=f"Обща цена: {total_price:.2f} лв")
        
        product_combo.bind("<<ComboboxSelected>>", lambda e: calculate_price())
        quantity_entry.bind("<KeyRelease>", lambda e: calculate_price())
        
        price_label = ttk.Label(sale_win, text="Обща цена: 0.00 лв")
        price_label.grid(row=3, columnspan=2, pady=5)
        
        def save_sale():
            try:
                client_id = client_combo.get().split(" - ")[0]
                product_id = product_combo.get().split(" - ")[0]
                quantity = int(quantity_entry.get())
                price = get_product_price(product_id)
                
                if quantity <= 0:
                    messagebox.showerror("Грешка", "Количеството трябва да е положително число!")
                    return
                
                new_id = generate_id("SL", sales)
                today = datetime.date.today().strftime("%d.%m.%Y")
                
                new_sale = {
                    "id": new_id,
                    "client_id": client_id,
                    "product_id": product_id,
                    "date": today,
                    "price": price,
                    "quantity": quantity
                }
                
                sales.append(new_sale)
                save_sales()
                messagebox.showinfo("Успех", "Продажбата е добавена успешно!")
                sale_win.destroy()
                update_list()  
            except ValueError:
                messagebox.showerror("Грешка", "Невалидни данни!")
        
        ttk.Button(sale_win, text="Запази", command=save_sale).grid(row=4, columnspan=2, pady=10)
    
    btn_frame = ttk.Frame(win)
    btn_frame.pack(fill=tk.X, pady=5)
    
    ttk.Button(btn_frame, text="Добави продажба", command=add_sale).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Обнови", command=update_list).pack(side=tk.LEFT, padx=5)
    

    update_list()
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    

    total_frame = ttk.Frame(win)
    total_frame.pack(fill=tk.X, pady=5)
    
    total_label = ttk.Label(total_frame, text="Общо: 0.00 лв", font=('Arial', 12, 'bold'))
    total_label.pack(side=tk.RIGHT, padx=10)
    

    def add_sale():
        sale_win = tk.Toplevel()
        sale_win.title("Нова продажба")
        
        ttk.Label(sale_win, text="Клиент:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        client_combo = ttk.Combobox(sale_win, values=[f"{c['id']} - {c['name']}" for c in clients])
        client_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(sale_win, text="Продукт:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        product_combo = ttk.Combobox(sale_win, values=[f"{p['id']} - {p['model']}" for p in products])
        product_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(sale_win, text="Количество:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        quantity_entry = ttk.Entry(sale_win)
        quantity_entry.insert(0, "1")
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def calculate_price():
            product_id = product_combo.get().split(" - ")[0]
            price = get_product_price(product_id)
            quantity = int(quantity_entry.get())
            total_price = price * quantity
            price_label.config(text=f"Обща цена: {total_price:.2f} лв")
        
        product_combo.bind("<<ComboboxSelected>>", lambda e: calculate_price())
        quantity_entry.bind("<KeyRelease>", lambda e: calculate_price())
        
        price_label = ttk.Label(sale_win, text="Обща цена: 0.00 лв")
        price_label.grid(row=3, columnspan=2, pady=5)
        
        def save_sale():
            try:
                client_id = client_combo.get().split(" - ")[0]
                product_id = product_combo.get().split(" - ")[0]
                quantity = int(quantity_entry.get())
                price = get_product_price(product_id)
                
                if quantity <= 0:
                    messagebox.showerror("Грешка", "Количеството трябва да е положително число!")
                    return
                
                new_id = generate_id("SL", sales)
                today = datetime.date.today().strftime("%d.%m.%Y")
                
                new_sale = {
                    "id": new_id,
                    "client_id": client_id,
                    "product_id": product_id,
                    "date": today,
                    "price": price,
                    "quantity": quantity
                }
                
                sales.append(new_sale)
                save_sales()
                messagebox.showinfo("Успех", "Продажбата е добавена успешно!")
                sale_win.destroy()
                update_list()
            except ValueError:
                messagebox.showerror("Грешка", "Невалидни данни!")
        
        ttk.Button(sale_win, text="Запази", command=save_sale).grid(row=4, columnspan=2, pady=10)
    

def show_all_repairs():
    win = tk.Toplevel()
    win.title("Всички ремонти")
    win.geometry("1000x600")
    

    filter_frame = ttk.Frame(win)
    filter_frame.pack(pady=10, fill=tk.X)
    
    ttk.Label(filter_frame, text="От дата:").pack(side=tk.LEFT)
    date_from = ttk.Entry(filter_frame, width=10)
    date_from.pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="До дата:").pack(side=tk.LEFT, padx=(10,0))
    date_to = ttk.Entry(filter_frame, width=10)
    date_to.pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="Клиент:").pack(side=tk.LEFT, padx=(10,0))
    client_combo = ttk.Combobox(filter_frame, values=["Всички"] + [f"{c['id']} - {c['name']}" for c in clients])
    client_combo.pack(side=tk.LEFT)
    client_combo.current(0)
    
    ttk.Label(filter_frame, text="Статус:").pack(side=tk.LEFT, padx=(10,0))
    status_combo = ttk.Combobox(filter_frame, values=["Всички", "Активни", "Завършени"])
    status_combo.pack(side=tk.LEFT)
    status_combo.current(0)
    
    def update_list():
        date_f = date_from.get()
        date_t = date_to.get()
        client = client_combo.get().split(" - ")[0] if client_combo.get() != "Всички" else None
        status = status_combo.get()
        
        tree.delete(*tree.get_children())
        total = 0
        for r in repairs:
            if ((not date_f or r['date'] >= date_f) and 
                (not date_t or r['date'] <= date_t) and 
                (not client or r['client_id'] == client)):
                
                client_name = get_client_name(r['client_id'])
                product_model = get_product_model(r['product_id'])
                total += r['price']
                tree.insert("", tk.END, values=(
                    r['id'], r['date'], client_name, product_model, 
                    r['desc'], f"{r['price']:.2f}"
                ))
        
        total_label.config(text=f"Общо: {total:.2f} лв")
    
    ttk.Button(filter_frame, text="Филтрирай", command=update_list).pack(side=tk.LEFT, padx=10)

    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("id", "date", "client", "product", "desc", "price"), 
                        show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("id", text="ID")
    tree.heading("date", text="Дата")
    tree.heading("client", text="Клиент")
    tree.heading("product", text="Продукт")
    tree.heading("desc", text="Описание")
    tree.heading("price", text="Цена")
    
    tree.column("id", width=80)
    tree.column("date", width=100)
    tree.column("client", width=150)
    tree.column("product", width=150)
    tree.column("desc", width=250)
    tree.column("price", width=100)
    
    update_list()
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    

    total_frame = ttk.Frame(win)
    total_frame.pack(fill=tk.X, pady=5)
    
    total_label = ttk.Label(total_frame, text="Общо: 0.00 лв", font=('Arial', 12, 'bold'))
    total_label.pack(side=tk.RIGHT, padx=10)
    

    def complete_repair():
        selected = tree.focus()
        if not selected:
            return
        repair_id = tree.item(selected)['values'][0]
        if messagebox.askyesno("Потвърждение", "Маркирате ремонта като завършен?"):
            messagebox.showinfo("Успех", "Ремонтът е маркиран като завършен!")
            update_list()
    
    menu = tk.Menu(win, tearoff=0)
    menu.add_command(label="Завърши ремонт", command=complete_repair)
    
    def show_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.focus(item)
            menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", show_menu)

def add_repair():
    win = tk.Toplevel()
    win.title("Добавяне на ремонт")
    win.geometry("500x400")
    
    ttk.Label(win, text="Клиент:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
    client_combo = ttk.Combobox(win, values=[f"{c['id']} - {c['name']}" for c in clients])
    client_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    
    ttk.Label(win, text="Продукт:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    product_combo = ttk.Combobox(win, values=[f"{p['id']} - {p['model']}" for p in products])
    product_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    
    ttk.Label(win, text="Описание на проблема:").grid(row=2, column=0, sticky=tk.NE, padx=5, pady=5)
    desc_text = tk.Text(win, height=5, width=30)
    desc_text.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    
    ttk.Label(win, text="Цена:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
    price_entry = ttk.Entry(win)
    price_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    
    def save_repair():
        try:
            client_id = client_combo.get().split(" - ")[0]
            product_id = product_combo.get().split(" - ")[0]
            description = desc_text.get("1.0", tk.END).strip()
            price = float(price_entry.get())
            
            if not description:
                messagebox.showerror("Грешка", "Моля, въведете описание на проблема!")
                return
            
            new_id = generate_id("RP", repairs)
            today = datetime.date.today().strftime("%d.%m.%Y")
            
            new_repair = {
                "id": new_id,
                "client_id": client_id,
                "product_id": product_id,
                "date": today,
                "desc": description,
                "price": price
            }
            
            repairs.append(new_repair)
            save_repairs()
            messagebox.showinfo("Успех", f"Ремонтът е добавен успешно с ID: {new_id}")
            win.destroy()
        except ValueError:
            messagebox.showerror("Грешка", "Невалидна цена!")
    
    ttk.Button(win, text="Запази", command=save_repair).grid(row=4, columnspan=2, pady=10)

def client_repairs():
    win = tk.Toplevel()
    win.title("Ремонти по клиент")
    win.geometry("800x500")
    
    ttk.Label(win, text="Изберете клиент:").pack(pady=10)
    combo = ttk.Combobox(win, values=[f"{c['id']} - {c['name']}" for c in clients])
    combo.pack()
    
    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("date", "product", "desc", "price"), 
                         show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("date", text="Дата")
    tree.heading("product", text="Продукт")
    tree.heading("desc", text="Описание")
    tree.heading("price", text="Цена")
    
    tree.column("date", width=100)
    tree.column("product", width=150)
    tree.column("desc", width=300)
    tree.column("price", width=100)
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    
    total_label = ttk.Label(win, text="Общо: 0.00 лв", font=('Arial', 12, 'bold'))
    total_label.pack(pady=5)
    
    def show():
        tree.delete(*tree.get_children())
        selected = combo.get().split(" - ")[0]
        total = 0
        for r in repairs:
            if r['client_id'] == selected:
                model = get_product_model(r['product_id'])
                total += r['price']
                tree.insert("", tk.END, values=(r['date'], model, r['desc'], f"{r['price']:.2f}"))
        
        total_label.config(text=f"Общо: {total:.2f} лв")
    
    combo.bind("<<ComboboxSelected>>", lambda e: show())

def search_sales_by_date():
    win = tk.Toplevel()
    win.title("Продажби по дата")
    win.geometry("800x500")
    
    dates = sorted(set(s['date'] for s in sales), reverse=True)
    
    ttk.Label(win, text="Изберете дата:").pack(pady=10)
    combo = ttk.Combobox(win, values=dates)
    combo.pack()
    
    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("client", "product", "price", "quantity", "total"), 
                         show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("client", text="Клиент")
    tree.heading("product", text="Продукт")
    tree.heading("price", text="Ед. цена")
    tree.heading("quantity", text="Количество")
    tree.heading("total", text="Общо")
    
    tree.column("client", width=150)
    tree.column("product", width=150)
    tree.column("price", width=100)
    tree.column("quantity", width=80)
    tree.column("total", width=100)
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    
    total_label = ttk.Label(win, text="Общо за деня: 0.00 лв", font=('Arial', 12, 'bold'))
    total_label.pack(pady=5)
    
    def show():
        tree.delete(*tree.get_children())
        date = combo.get()
        daily_total = 0
        for s in sales:
            if s['date'] == date:
                client_name = get_client_name(s['client_id'])
                model = get_product_model(s['product_id'])
                sale_total = s['price'] * s['quantity']
                daily_total += sale_total
                tree.insert("", tk.END, values=(
                    client_name, model, f"{s['price']:.2f}", 
                    s['quantity'], f"{sale_total:.2f}"
                ))
        
        total_label.config(text=f"Общо за деня: {daily_total:.2f} лв")
    
    combo.bind("<<ComboboxSelected>>", lambda e: show())

def filter_products_by_type():
    win = tk.Toplevel()
    win.title("Филтриране на продукти")
    win.geometry("700x500")
    
    types = sorted(set(p['type'] for p in products))
    brands = sorted(set(p['brand'] for p in products))
    
    ttk.Label(win, text="Тип продукт:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    type_combo = ttk.Combobox(win, values=["Всички"] + types)
    type_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    type_combo.current(0)
    
    ttk.Label(win, text="Марка:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    brand_combo = ttk.Combobox(win, values=["Всички"] + brands)
    brand_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    brand_combo.current(0)
    
    ttk.Label(win, text="Цена от:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    price_from = ttk.Entry(win, width=10)
    price_from.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    
    ttk.Label(win, text="до:").grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    price_to = ttk.Entry(win, width=10)
    price_to.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
    
    ttk.Label(win, text="Сортиране:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    sort_combo = ttk.Combobox(win, values=["По ID", "По име (А-Я)", "По име (Я-А)", "По цена (възх.)", "По цена (низх.)"])
    sort_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    sort_combo.current(0)
    
    tree_frame = ttk.Frame(win)
    tree_frame.grid(row=4, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("model", "type", "brand", "price"), 
                         show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("model", text="Модел")
    tree.heading("type", text="Тип")
    tree.heading("brand", text="Марка")
    tree.heading("price", text="Цена")
    
    tree.column("model", width=200)
    tree.column("type", width=150)
    tree.column("brand", width=150)
    tree.column("price", width=100)
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    
    win.grid_rowconfigure(4, weight=1)
    win.grid_columnconfigure(1, weight=1)
    
    def apply_filters():
        tree.delete(*tree.get_children())
        type_ = type_combo.get()
        brand = brand_combo.get()
        
        try:
            price_min = float(price_from.get()) if price_from.get() else 0
            price_max = float(price_to.get()) if price_to.get() else float('inf')
        except ValueError:
            messagebox.showerror("Грешка", "Невалидна цена!")
            return
        
        filtered = [p for p in products 
                   if (type_ == "Всички" or p['type'] == type_)
                   and (brand == "Всички" or p['brand'] == brand)
                   and (price_min <= p['price'] <= price_max)]
        

        sort_by = sort_combo.get()
        if sort_by == "По име (А-Я)":
            filtered.sort(key=lambda x: x['model'])
        elif sort_by == "По име (Я-А)":
            filtered.sort(key=lambda x: x['model'], reverse=True)
        elif sort_by == "По цена (възх.)":
            filtered.sort(key=lambda x: x['price'])
        elif sort_by == "По цена (низх.)":
            filtered.sort(key=lambda x: x['price'], reverse=True)
        
        for p in filtered:
            tree.insert("", tk.END, values=(p['model'], p['type'], p['brand'], f"{p['price']:.2f}"))
    
    ttk.Button(win, text="Филтрирай", command=apply_filters).grid(row=5, columnspan=2, pady=10)
    apply_filters()

def client_report():
    win = tk.Toplevel()
    win.title("Справка за клиент")
    win.geometry("800x600")
    
    ttk.Label(win, text="Изберете клиент:").pack(pady=10)
    combo = ttk.Combobox(win, values=[f"{c['id']} - {c['name']}" for c in clients])
    combo.pack()
    
    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    

    repairs_frame = ttk.Frame(notebook)
    notebook.add(repairs_frame, text="Ремонти")
    
    repairs_tree = ttk.Treeview(repairs_frame, columns=("date", "product", "desc", "price"), show="headings")
    repairs_tree.heading("date", text="Дата")
    repairs_tree.heading("product", text="Продукт")
    repairs_tree.heading("desc", text="Описание")
    repairs_tree.heading("price", text="Цена")
    
    repairs_tree.column("date", width=100)
    repairs_tree.column("product", width=150)
    repairs_tree.column("desc", width=300)
    repairs_tree.column("price", width=100)
    
    repairs_tree.pack(expand=True, fill=tk.BOTH)
    
    repairs_total = ttk.Label(repairs_frame, text="Общо за ремонти: 0.00 лв", font=('Arial', 12, 'bold'))
    repairs_total.pack(pady=5)
    

    sales_frame = ttk.Frame(notebook)
    notebook.add(sales_frame, text="Продажби")
    
    sales_tree = ttk.Treeview(sales_frame, columns=("date", "product", "price", "quantity", "total"), show="headings")
    sales_tree.heading("date", text="Дата")
    sales_tree.heading("product", text="Продукт")
    sales_tree.heading("price", text="Ед. цена")
    sales_tree.heading("quantity", text="Количество")
    sales_tree.heading("total", text="Общо")
    
    sales_tree.column("date", width=100)
    sales_tree.column("product", width=150)
    sales_tree.column("price", width=100)
    sales_tree.column("quantity", width=80)
    sales_tree.column("total", width=100)
    
    sales_tree.pack(expand=True, fill=tk.BOTH)
    
    sales_total = ttk.Label(sales_frame, text="Общо за продажби: 0.00 лв", font=('Arial', 12, 'bold'))
    sales_total.pack(pady=5)
    

    overall_total = ttk.Label(win, text="Общо за клиента: 0.00 лв", font=('Arial', 14, 'bold'))
    overall_total.pack(pady=10)
    
    def generate_report():
        selected_id = combo.get().split(" - ")[0]
        client = next((c for c in clients if c['id'] == selected_id), None)
        if not client:
            return

        client_repairs = [r for r in repairs if r['client_id'] == selected_id]
        repairs_tree.delete(*repairs_tree.get_children())
        repairs_sum = 0
        for r in client_repairs:
            model = get_product_model(r['product_id'])
            repairs_sum += r['price']
            repairs_tree.insert("", tk.END, values=(r['date'], model, r['desc'], f"{r['price']:.2f}"))
        repairs_total.config(text=f"Общо за ремонти: {repairs_sum:.2f} лв")

        client_sales = [s for s in sales if s['client_id'] == selected_id]
        sales_tree.delete(*sales_tree.get_children())
        sales_sum = 0
        for s in client_sales:
            model = get_product_model(s['product_id'])
            total = s['price'] * s['quantity']
            sales_sum += total
            sales_tree.insert("", tk.END, values=(
                s['date'], model, f"{s['price']:.2f}", s['quantity'], f"{total:.2f}"
            ))
        sales_total.config(text=f"Общо за продажби: {sales_sum:.2f} лв")
        

        overall = repairs_sum + sales_sum
        overall_total.config(text=f"Общо за клиента: {overall:.2f} лв")
        

    ttk.Button(win, text="Генерирай справка", command=generate_report).pack(pady=10)
    ttk.Button(win, text="Запази като файл", command=lambda: save_report_to_file(combo.get())).pack(pady=5)

def show_all_repairs():
    win = tk.Toplevel()
    win.title("Всички ремонти")
    win.geometry("1000x600")
    

    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("id", "date", "client", "product", "desc", "price"), 
                         show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("id", text="ID")
    tree.heading("date", text="Дата")
    tree.heading("client", text="Клиент")
    tree.heading("product", text="Продукт")
    tree.heading("desc", text="Описание")
    tree.heading("price", text="Цена")
    
    tree.column("id", width=80)
    tree.column("date", width=100)
    tree.column("client", width=150)
    tree.column("product", width=150)
    tree.column("desc", width=300)
    tree.column("price", width=100)
    
    for r in repairs:
        client_name = get_client_name(r['client_id'])
        product_model = get_product_model(r['product_id'])
        tree.insert("", tk.END, values=(
            r['id'], r['date'], client_name, product_model, 
            r['desc'], f"{r['price']:.2f}"
        ))
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    

    filter_frame = ttk.Frame(win)
    filter_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(filter_frame, text="Филтри:").pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="Клиент:").pack(side=tk.LEFT, padx=5)
    client_combo = ttk.Combobox(filter_frame, values=["Всички"] + [c['name'] for c in clients])
    client_combo.pack(side=tk.LEFT)
    client_combo.current(0)
    
    ttk.Label(filter_frame, text="От дата:").pack(side=tk.LEFT, padx=5)
    date_from = ttk.Entry(filter_frame, width=10)
    date_from.pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="До дата:").pack(side=tk.LEFT, padx=5)
    date_to = ttk.Entry(filter_frame, width=10)
    date_to.pack(side=tk.LEFT)
    
    def apply_filters():
        client_filter = client_combo.get()
        date_f = date_from.get()
        date_t = date_to.get()
        
        tree.delete(*tree.get_children())
        for r in repairs:
            match_client = client_filter == "Всички" or get_client_name(r['client_id']) == client_filter
            match_date = (not date_f or r['date'] >= date_f) and (not date_t or r['date'] <= date_t)
            
            if match_client and match_date:
                client_name = get_client_name(r['client_id'])
                product_model = get_product_model(r['product_id'])
                tree.insert("", tk.END, values=(
                    r['id'], r['date'], client_name, product_model, 
                    r['desc'], f"{r['price']:.2f}"
                ))
    
    ttk.Button(filter_frame, text="Приложи филтри", command=apply_filters).pack(side=tk.LEFT, padx=10)

def search_sales_by_date():
    win = tk.Toplevel()
    win.title("Продажби по дата")
    win.geometry("900x600")
    

    dates = sorted(set(s['date'] for s in sales), reverse=True)
    
    filter_frame = ttk.Frame(win)
    filter_frame.pack(pady=10, fill=tk.X)
    
    ttk.Label(filter_frame, text="Изберете дата:").pack(side=tk.LEFT)
    date_combo = ttk.Combobox(filter_frame, values=["Всички"] + dates)
    date_combo.pack(side=tk.LEFT, padx=5)
    date_combo.current(0)
    

    ttk.Label(filter_frame, text="или период от:").pack(side=tk.LEFT, padx=5)
    date_from = ttk.Entry(filter_frame, width=10)
    date_from.pack(side=tk.LEFT)
    
    ttk.Label(filter_frame, text="до:").pack(side=tk.LEFT)
    date_to = ttk.Entry(filter_frame, width=10)
    date_to.pack(side=tk.LEFT)
    
    tree_frame = ttk.Frame(win)
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(tree_frame, columns=("date", "client", "product", "price", "quantity", "total"), 
                         show="headings", yscrollcommand=scrollbar.set)
    
    tree.heading("date", text="Дата")
    tree.heading("client", text="Клиент")
    tree.heading("product", text="Продукт")
    tree.heading("price", text="Ед. цена")
    tree.heading("quantity", text="Количество")
    tree.heading("total", text="Общо")
    
    tree.column("date", width=100)
    tree.column("client", width=150)
    tree.column("product", width=150)
    tree.column("price", width=100)
    tree.column("quantity", width=80)
    tree.column("total", width=100)
    
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=tree.yview)
    
    total_label = ttk.Label(win, text="Общо: 0.00 лв", font=('Arial', 12, 'bold'))
    total_label.pack(pady=5)
    
    def show_sales():
        tree.delete(*tree.get_children())
        selected_date = date_combo.get()
        date_f = date_from.get()
        date_t = date_to.get()
        total = 0
        
        for s in sales:
            if (selected_date == "Всички" or s['date'] == selected_date) or \
               (date_f and date_t and date_f <= s['date'] <= date_t):
                client_name = get_client_name(s['client_id'])
                model = get_product_model(s['product_id'])
                sale_total = s['price'] * s['quantity']
                total += sale_total
                tree.insert("", tk.END, values=(
                    s['date'], client_name, model, f"{s['price']:.2f}", 
                    s['quantity'], f"{sale_total:.2f}"
                ))
        
        total_label.config(text=f"Общо: {total:.2f} лв")
    
    date_combo.bind("<<ComboboxSelected>>", lambda e: show_sales())
    ttk.Button(filter_frame, text="Покажи", command=show_sales).pack(side=tk.LEFT, padx=10)
    

    show_sales()

def save_report_to_file(client_info):
    if not client_info:
        messagebox.showerror("Грешка", "Моля, изберете клиент първо!")
        return
    
    client_id = client_info.split(" - ")[0]
    client = next((c for c in clients if c['id'] == client_id), None)
    if not client:
        return
    

    client_repairs = [r for r in repairs if r['client_id'] == client_id]
    client_sales = [s for s in sales if s['client_id'] == client_id]
    
    repairs_sum = sum(r['price'] for r in client_repairs)
    sales_sum = sum(s['price'] * s['quantity'] for s in client_sales)
    overall = repairs_sum + sales_sum
    

    content = f"Справка за клиент: {client['name']}\n"
    content += f"Телефон: {client['phone']}\n"
    content += f"Имейл: {client['email']}\n\n"
    
    content += "Ремонти:\n"
    for r in client_repairs:
        product = get_product_model(r['product_id'])
        content += f"{r['date']} - {product} - {r['desc']} - {r['price']:.2f} лв\n"
    content += f"\nОбщо ремонти: {len(client_repairs)} на стойност {repairs_sum:.2f} лв\n\n"
    
    content += "Продажби:\n"
    for s in client_sales:
        product = get_product_model(s['product_id'])
        total = s['price'] * s['quantity']
        content += f"{s['date']} - {product} - {s['quantity']} x {s['price']:.2f} = {total:.2f} лв\n"
    content += f"\nОбщо продажби: {len(client_sales)} на стойност {sales_sum:.2f} лв\n\n"
    
    content += f"ОБЩО: {overall:.2f} лв\n"
    

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстови файлове", "*.txt"), ("Всички файлове", "*.*")],
        initialfile=f"spravka_{client_id}.txt"
    )
    
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Успех", f"Справката е запазена във файл:\n{file_path}")
    

def show_statistics():
    win = tk.Toplevel()
    win.title("Статистика")
    win.geometry("600x400")
    
    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill=tk.BOTH)
    

    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="Обща")
    
    stats = [
        f"Общо клиенти: {len(clients)}",
        f"Общо продукти: {len(products)}",
        f"Общо продажби: {len(sales)}",
        f"Общо ремонти: {len(repairs)}",
        "",
        f"Общо приходи от продажби: {sum(s['price'] * s['quantity'] for s in sales):.2f} лв",
        f"Общо приходи от ремонти: {sum(r['price'] for r in repairs):.2f} лв",
        f"Общо приходи: {sum(s['price'] * s['quantity'] for s in sales) + sum(r['price'] for r in repairs):.2f} лв"
    ]
    
    for i, stat in enumerate(stats):
        ttk.Label(general_frame, text=stat).pack(anchor=tk.W, padx=10, pady=5)
    

    monthly_frame = ttk.Frame(notebook)
    notebook.add(monthly_frame, text="Месечна")
    
    # евентуално да я добавя по нататък ! 
    ttk.Label(monthly_frame, text="Не съм я направил още.. но ако реша да развивам кода, ще я! ").pack(pady=50)
    

    products_frame = ttk.Frame(notebook)
    notebook.add(products_frame, text="Продукти")
    
        # евентуално да ще го добавя по нататък !
    ttk.Label(products_frame, text="Не съм го направил още.. но ако реша да развивам кода, ще я! ").pack(pady=50)

def generate_receipt():
    win = tk.Toplevel()
    win.title("Генериране на касова бележка")
    win.geometry("500x400")
    
    ttk.Label(win, text="Тип транзакция:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    type_combo = ttk.Combobox(win, values=["Продажба", "Ремонт"])
    type_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    type_combo.current(0)
    
    ttk.Label(win, text="Номер на транзакция:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    id_combo = ttk.Combobox(win)
    id_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    
    receipt_text = tk.Text(win, height=15, width=50)
    receipt_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    def update_ids():
        trans_type = type_combo.get()
        if trans_type == "Продажба":
            ids = [s['id'] for s in sales]
        else:
            ids = [r['id'] for r in repairs]
        id_combo['values'] = ids
        if ids:
            id_combo.current(0)
            update_receipt()
    
    def update_receipt():
        trans_type = type_combo.get()
        trans_id = id_combo.get()
        
        if not trans_id:
            return
        
        receipt_text.delete("1.0", tk.END)
        
        today = datetime.date.today().strftime("%d.%m.%Y")
        now = datetime.datetime.now().strftime("%H:%M:%S")
        
        receipt_text.insert(tk.END, "КОМПЮТЪРЕН СЕРВИЗ\n")
        receipt_text.insert(tk.END, "ул. .... ... ....\n")
        receipt_text.insert(tk.END, "Тел: +359 ... ... ...\n")
        receipt_text.insert(tk.END, f"Дата: {today} Час: {now}\n")
        receipt_text.insert(tk.END, f"Касов бон №: {trans_id}\n")
        receipt_text.insert(tk.END, "="*40 + "\n")
        
        if trans_type == "Продажба":
            sale = next((s for s in sales if s['id'] == trans_id), None)
            if sale:
                product = next((p for p in products if p['id'] == sale['product_id']), None)
                client = next((c for c in clients if c['id'] == sale['client_id']), None)
                
                receipt_text.insert(tk.END, f"Клиент: {client['name'] if client else 'Неизвестен'}\n")
                receipt_text.insert(tk.END, f"Продукт: {product['model'] if product else 'Неизвестен'}\n")
                receipt_text.insert(tk.END, f"Количество: {sale['quantity']}\n")
                receipt_text.insert(tk.END, f"Ед. цена: {sale['price']:.2f} лв\n")
                receipt_text.insert(tk.END, "="*40 + "\n")
                receipt_text.insert(tk.END, f"ОБЩО: {sale['price'] * sale['quantity']:.2f} лв\n")
        else:
            repair = next((r for r in repairs if r['id'] == trans_id), None)
            if repair:
                product = next((p for p in products if p['id'] == repair['product_id']), None)
                client = next((c for c in clients if c['id'] == repair['client_id']), None)
                
                receipt_text.insert(tk.END, f"Клиент: {client['name'] if client else 'Неизвестен'}\n")
                receipt_text.insert(tk.END, f"Продукт: {product['model'] if product else 'Неизвестен'}\n")
                receipt_text.insert(tk.END, f"Описание: {repair['desc']}\n")
                receipt_text.insert(tk.END, "="*40 + "\n")
                receipt_text.insert(tk.END, f"ОБЩО: {repair['price']:.2f} лв\n")
        
        receipt_text.insert(tk.END, "="*40 + "\n")
        receipt_text.insert(tk.END, "Благодарим Ви, че използвате нашите услуги!\n")
    
    type_combo.bind("<<ComboboxSelected>>", lambda e: update_ids())
    id_combo.bind("<<ComboboxSelected>>", lambda e: update_receipt())
    
    def print_receipt():

        messagebox.showinfo("Успех", "Касовият бон е готов за печат!")
    
    ttk.Button(win, text="Печат", command=print_receipt).grid(row=3, column=0, pady=10)
    ttk.Button(win, text="Запази като текст", command=lambda: save_receipt_to_file(receipt_text.get("1.0", tk.END))).grid(row=3, column=1, pady=10)
    
    update_ids()

def save_receipt_to_file(receipt_text):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстови файлове", "*.txt"), ("Всички файлове", "*.*")],
        initialfile=f"receipt_{datetime.date.today().strftime('%Y%m%d')}.txt"
    )
    
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(receipt_text)
        messagebox.showinfo("Успех", f"Касовият бон е запазен във файл:\n{file_path}")


if __name__ == "__main__":

    if not os.path.exists("КомпСервиз"):
        os.makedirs("КомпСервиз")
    
    load_all()
    login_screen()