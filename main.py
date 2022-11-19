import psycopg2
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class LoginView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('350x220+650+300')
        self.root.title('Login')
        self.root.config(bg="#dbdbdb")

        self.Label_Name = tk.Label(self.root, text="Name", font=("times new roman", 14), bg="#dbdbdb")
        self.Label_Password = tk.Label(self.root, text="Password", font=("times new roman", 14), bg="#dbdbdb")
        self.Label_Name.place(x=90, y=50)
        self.Label_Password.place(x=60, y=80)

        self.Entry_Name = tk.Entry(self.root)
        self.Entry_Password = tk.Entry(self.root)
        self.Entry_Name.place(x=150, y=50)
        self.Entry_Password.place(x=150, y=80)

        self.Button_Log = tk.Button(self.root, text="Login", width=15, height=2,
                                    command=self.Button_Connection)
        self.Button_Log.place(x=120, y=130)

        self.root.mainloop()
        # messagebox.showwarning(title='Error', message=ex_)

    def Button_Connection(self):
        try:
            Name = self.Entry_Name.get()
            Password = self.Entry_Password.get()
            global conn
            conn = psycopg2.connect(user='postgres', password='ABC1241',  # postgres ABC1241 SMMMJ Dgt5Re1 Name Password
                                    host='localhost', port=5432, database='DataBase')

        except Exception as _ex:
            messagebox.showwarning(title='Error', message=['Ошибка авторизации'])
        else:
            print('Connect')
            self.root.destroy()
            TableView()


class TableView:
    def __init__(self):
        global Table
        Table = '1'
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.root = tk.Tk()
        self.root.geometry('1300x650+350+300')
        self.root.title('Table')
        self.root.config(bg="#dbdbdb")

        # self.root.rowconfigure()index=0, weight=1

        self.root.option_add("*tearOff", FALSE)
        self.file_menu = Menu()
        self.file_menu.add_command(label='Машины', command=self.Table1)
        self.file_menu.add_command(label='Аренда авто.', command=self.Table2)
        self.file_menu.add_command(label='Штрафы', command=self.Table3)
        self.file_menu.add_command(label='Клиент', command=self.Table4)
        self.file_menu.add_command(label='Сотрудник', command=self.Table5)

        self.main_menu = Menu()
        self.main_menu.add_cascade(label='Table', menu=self.file_menu)
        self.main_menu.add_cascade(label='Exit', command=self.Exit)

        self.Search_Entry = tk.Entry()
        self.Search_Entry.place(x=1150, y=40)

        self.Label_Search = tk.Label(self.root, text="Поиск по id:", font=("times new roman", 10), bg="#dbdbdb")
        self.Label_Search.place(x=1150, y=15)

        self.Search_Button = tk.Button(text='Search', command=self.Search)
        self.Create_Button = tk.Button(text='Create', command=self.Create)
        self.Delete_Button = tk.Button(text='Delete', command=self.Delete)
        self.Search_Button.place(x=1150, y=65)
        self.Create_Button.place(x=1150, y=95)
        self.Delete_Button.place(x=1150, y=125)

        self.root.config(menu=self.main_menu)
        self.root.mainloop()

    def Exit(self):
        print('Exit. Connect close.')
        conn.close()
        self.root.destroy()
        LoginView()

    def Search(self):
        Table = self.Table
        Search = self.Search_Entry.get()
        self.Search_Entry.delete(0, 'end')
        if Table == 'car':
            if Search.isdigit() == True:
                self.cursor.execute(
                    """Select car_id,car_brand,car_model,year_of_release,cost_per_day,condition,state_number,toc.id_type,
                    toc.type_of_car,toc.transmission_type
                    From %s c
                    INNER JOIN type_of_car toc ON c.id_type = toc.id_type
                    WHERE car_id = %%s                     
                    ORDER BY car_id;""" % Table, Search
                )
            else:
                messagebox.showwarning(title='Error', message=['Неправильный тип данных'])
                return

            conn.commit()
            row = self.cursor.fetchall()

            columns = ["id машины", "Бренд", "Модель", "Год выпуска", "Стоимость за день", "Состояние", "Гос.номер",
                       "Тип авто.", "Тип трансмиссии"]

            self.root.rowconfigure(index=0, weight=1)  #
            self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
            self.tree.grid(row=0, column=0, sticky="nsew")

            # определяем заголовки с выпавниваем по левому краю
            self.tree.heading("id машины", text="id машины", anchor=W)
            self.tree.heading("Бренд", text="Бренд", anchor=W)
            self.tree.heading("Модель", text="Модель", anchor=W)
            self.tree.heading("Год выпуска", text="Год выпуска", anchor=W)
            self.tree.heading("Стоимость за день", text="Стоимость за день", anchor=W)
            self.tree.heading("Состояние", text="Состояние", anchor=W)
            self.tree.heading("Гос.номер", text="Гос. номер", anchor=W)
            self.tree.heading("Тип авто.", text="Тип авто.", anchor=W)
            self.tree.heading("Тип трансмиссии", text="Тип трансмиссии", anchor=W)

            # настраиваем столбцы
            self.tree.column("#1", stretch=NO, width=75)
            self.tree.column("#2", stretch=NO, width=60)
            self.tree.column("#3", stretch=NO, width=120)
            self.tree.column("#4", stretch=NO, width=80)
            self.tree.column("#5", stretch=NO, width=70)
            self.tree.column("#6", stretch=NO, width=90)
            self.tree.column("#7", stretch=NO, width=90)
            self.tree.column("#8", stretch=NO, width=80)
            self.tree.column("#9", stretch=NO, width=150)

            for person in row:
                self.tree.insert("", END, values=person)

            self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        elif Table == 'car_rental':
            if Search.isdigit() == True:
                self.cursor.execute(
                    """Select cr.rental_id,cr.client_id,cr.car_id,cr.employee_id,cr.date_issue_car,cr.number_of_days,
                    cr.return_date,cr.amount,ds.name_of_discounts,rp.number_of_fines,rp.amount_of_fines,cr.finite_sum
                    FROM %s cr
                    INNER JOIN discount_system  ds ON ds.discount_id = cr.discount_id
                    INNER JOIN rental_penalties rp ON rp.id_of_rental_fines = cr.id_of_rental_fines
                    WHERE cr.rental_id = %%s
                    ORDER BY cr.rental_id;""" % Table, Search
                )
            else:
                messagebox.showwarning(title='Error', message=['Неправильный тип данных'])
                return
            conn.commit()
            row = self.cursor.fetchall()

            columns = ["rental_id", "client_id", "car_id", "employee_id", "date_issue_car", "number_of_days",
                       "return_date", "amount", "name_of_discounts", "number_of_fines", "amount_of_fines", "finite_sum"]

            self.root.rowconfigure(index=0, weight=1)  #
            self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
            self.tree.grid(row=0, column=0, sticky="nsew")
            # self.tree.pack(fill=BOTH, expand=1)

            # определяем заголовки с выпавниваем по левому краю
            self.tree.heading("rental_id", text="id Аренды", anchor=W)
            self.tree.heading("client_id", text="id Клиена", anchor=W)
            self.tree.heading("car_id", text="id Авто.", anchor=W)
            self.tree.heading("employee_id", text="id Сотрудника", anchor=W)
            self.tree.heading("date_issue_car", text="Дата выдачи авто.", anchor=W)
            self.tree.heading("number_of_days", text="Количество дней", anchor=W)
            self.tree.heading("return_date", text="Дата возврата", anchor=W)
            self.tree.heading("amount", text="Сумма", anchor=W)
            self.tree.heading("name_of_discounts", text="Скидка", anchor=W)
            self.tree.heading("number_of_fines", text="Количество штрафов", anchor=W)
            self.tree.heading("amount_of_fines", text="Сумма штрафов", anchor=W)
            self.tree.heading("finite_sum", text="Конечная сумма", anchor=W)

            # настраиваем столбцы
            self.tree.column("#1", stretch=NO, width=75)
            self.tree.column("#2", stretch=NO, width=75)
            self.tree.column("#3", stretch=NO, width=60)
            self.tree.column("#4", stretch=NO, width=90)
            self.tree.column("#5", stretch=NO, width=110)
            self.tree.column("#6", stretch=NO, width=110)
            self.tree.column("#7", stretch=NO, width=90)
            self.tree.column("#8", stretch=NO, width=70)
            self.tree.column("#9", stretch=NO, width=80)
            self.tree.column("#10", stretch=NO, width=130)
            self.tree.column("#11", stretch=NO, width=100)
            self.tree.column("#12", stretch=NO, width=100)

            for person in row:
                self.tree.insert("", END, values=person)

            self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        elif Table == 'penalties':
            if Search.isdigit() == True:
                self.cursor.execute(
                    """SELECT *    
                        FROM %s
                        WHERE id_of_rental_fines = %%s
                        ORDER BY penalties_id;""" % Table, Search
                )
            else:
                messagebox.showwarning(title='Error', message=['Неправильный тип данных'])
                return

            conn.commit()
            row = self.cursor.fetchall()

            columns = ["penalties_id", "id_of_rental_fines", "name_of_fine", "amount_of_penalty"]

            self.root.rowconfigure(index=0, weight=1)  #
            self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
            self.tree.grid(row=0, column=0, sticky="nsew")
            # self.tree.pack(fill=BOTH, expand=1)

            # определяем заголовки с выпавниваем по левому краю
            self.tree.heading("penalties_id", text="id Штрафа", anchor=W)
            self.tree.heading("id_of_rental_fines", text="id Аренды", anchor=W)
            self.tree.heading("name_of_fine", text="Название штрафа", anchor=W)
            self.tree.heading("amount_of_penalty", text="Сумма штрафа", anchor=W)

            # настраиваем столбцы
            self.tree.column("#1", stretch=NO, width=75)
            self.tree.column("#2", stretch=NO, width=80)
            self.tree.column("#3", stretch=NO, width=120)
            self.tree.column("#4", stretch=NO, width=100)

            for person in row:
                self.tree.insert("", END, values=person)

            self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        elif Table == 'client':
            if Search.isdigit() == True:
                self.cursor.execute(
                    """SELECT  client_id,name,surname,patronymic,phone,city
                        FROM %s
                        WHERE client_id = %%s
                        ORDER BY client_id;""" % Table, Search
                )
            else:
                messagebox.showwarning(title='Error', message=['Неправильный тип данных'])
                return

            conn.commit()
            row = self.cursor.fetchall()

            columns = ["client_id", "name", "surname", "patronymic", "phone", "city"]

            self.root.rowconfigure(index=0, weight=1)
            self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
            self.tree.grid(row=0, column=0, sticky="nsew")
            # self.tree.pack(fill=BOTH, expand=1)

            # определяем заголовки с выпавниваем по левому краю
            self.tree.heading("client_id", text="id Клиетна", anchor=W)
            self.tree.heading("name", text="Имя", anchor=W)
            self.tree.heading("surname", text="Фамилия", anchor=W)
            self.tree.heading("patronymic", text="Отчество", anchor=W)
            self.tree.heading("phone", text="Телефон", anchor=W)
            self.tree.heading("city", text="Город", anchor=W)

            # настраиваем столбцы
            self.tree.column("#1", stretch=NO, width=75)
            self.tree.column("#2", stretch=NO, width=60)
            self.tree.column("#3", stretch=NO, width=70)
            self.tree.column("#4", stretch=NO, width=80)
            self.tree.column("#5", stretch=NO, width=110)
            self.tree.column("#6", stretch=NO, width=100)

            for person in row:
                self.tree.insert("", END, values=person)

            self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        elif Table == 'employee':
            if Search.isdigit() == True:
                self.cursor.execute(
                    """SELECT employee_id,name,surname,patronymic,phone,city
                        FROM %s
                        WHERE employee_id = %%s
                        ORDER BY employee_id;""" % Table, Search
                )
            else:
                messagebox.showwarning(title='Error', message=['Неправильный тип данных'])
                return
            conn.commit()
            row = self.cursor.fetchall()

            columns = ["employee_id", "name", "surname", "patronymic", "phone", "city"]

            self.root.rowconfigure(index=0, weight=1)  #
            self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
            self.tree.grid(row=0, column=0, sticky="nsew")

            # определяем заголовки с выпавниваем по левому краю
            self.tree.heading("employee_id", text="id Сотрудника", anchor=W)
            self.tree.heading("name", text="Имя", anchor=W)
            self.tree.heading("surname", text="Фамилия", anchor=W)
            self.tree.heading("patronymic", text="Отчество", anchor=W)
            self.tree.heading("phone", text="Телефон", anchor=W)
            self.tree.heading("city", text="Город", anchor=W)

            # настраиваем столбцы
            self.tree.column("#1", stretch=NO, width=90)
            self.tree.column("#2", stretch=NO, width=80)
            self.tree.column("#3", stretch=NO, width=80)
            self.tree.column("#4", stretch=NO, width=80)
            self.tree.column("#5", stretch=NO, width=110)
            self.tree.column("#6", stretch=NO, width=100)

            for person in row:
                self.tree.insert("", END, values=person)

            self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky="ns")

        else:
            return

    def Table1(self):
        self.Table = 'car'  # Avto

        self.cursor.execute(
            """Select car_id,car_brand,car_model,year_of_release,cost_per_day,condition,state_number,toc.id_type,
                toc.type_of_car,toc.transmission_type
                From car c
                INNER JOIN type_of_car toc ON c.id_type = toc.id_type
                ORDER BY car_id;"""
        )
        conn.commit()
        row = self.cursor.fetchall()

        columns = ["id машины", "Бренд", "Модель", "Год выпуска", "Стоимость за день", "Состояние", "Гос.номер",
                   "Тип авто.", "Тип трансмиссии"]

        self.root.rowconfigure(index=0, weight=1)  #
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        # self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id машины", text="id машины", anchor=W)
        self.tree.heading("Бренд", text="Бренд", anchor=W)
        self.tree.heading("Модель", text="Модель", anchor=W)
        self.tree.heading("Год выпуска", text="Год выпуска", anchor=W)
        self.tree.heading("Стоимость за день", text="Стоимость за день", anchor=W)
        self.tree.heading("Состояние", text="Состояние", anchor=W)
        self.tree.heading("Гос.номер", text="Гос. номер", anchor=W)
        self.tree.heading("Тип авто.", text="Тип авто.", anchor=W)
        self.tree.heading("Тип трансмиссии", text="Тип трансмиссии", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=75)
        self.tree.column("#2", stretch=NO, width=60)
        self.tree.column("#3", stretch=NO, width=120)
        self.tree.column("#4", stretch=NO, width=80)
        self.tree.column("#5", stretch=NO, width=70)
        self.tree.column("#6", stretch=NO, width=90)
        self.tree.column("#7", stretch=NO, width=90)
        self.tree.column("#8", stretch=NO, width=80)
        self.tree.column("#9", stretch=NO, width=150)

        for person in row:
            self.tree.insert("", END, values=person)

        self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def Table2(self):
        global Table
        Table = 'car_rental'

        self.cursor.execute(
            """Select cr.rental_id,cr.client_id,cr.car_id,cr.employee_id,cr.date_issue_car,cr.number_of_days,
            cr.return_date,cr.amount,ds.name_of_discounts,rp.number_of_fines,rp.amount_of_fines,cr.finite_sum
            FROM car_rental cr
            INNER JOIN discount_system  ds ON ds.discount_id = cr.discount_id
            INNER JOIN rental_penalties rp ON rp.id_of_rental_fines = cr.id_of_rental_fines
            ORDER BY cr.rental_id;"""
        )
        conn.commit()
        row = self.cursor.fetchall()

        columns = ["rental_id", "client_id", "car_id", "employee_id", "date_issue_car", "number_of_days", "return_date",
                   "amount", "name_of_discounts", "number_of_fines", "amount_of_fines", "finite_sum"]

        self.root.rowconfigure(index=0, weight=1)  #
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        # self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("rental_id", text="id Аренды", anchor=W)
        self.tree.heading("client_id", text="id Клиена", anchor=W)
        self.tree.heading("car_id", text="id Авто.", anchor=W)
        self.tree.heading("employee_id", text="id Сотрудника", anchor=W)
        self.tree.heading("date_issue_car", text="Дата выдачи авто.", anchor=W)
        self.tree.heading("number_of_days", text="Количество дней", anchor=W)
        self.tree.heading("return_date", text="Дата возврата", anchor=W)
        self.tree.heading("amount", text="Сумма", anchor=W)
        self.tree.heading("name_of_discounts", text="Скидка", anchor=W)
        self.tree.heading("number_of_fines", text="Количество штрафов", anchor=W)
        self.tree.heading("amount_of_fines", text="Сумма штрафов", anchor=W)
        self.tree.heading("finite_sum", text="Конечная сумма", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=75)
        self.tree.column("#2", stretch=NO, width=75)
        self.tree.column("#3", stretch=NO, width=60)
        self.tree.column("#4", stretch=NO, width=90)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=110)
        self.tree.column("#7", stretch=NO, width=90)
        self.tree.column("#8", stretch=NO, width=70)
        self.tree.column("#9", stretch=NO, width=80)
        self.tree.column("#10", stretch=NO, width=130)
        self.tree.column("#11", stretch=NO, width=100)
        self.tree.column("#12", stretch=NO, width=100)

        for person in row:
            self.tree.insert("", END, values=person)

        self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def Table3(self):
        self.Table = 'penalties'  # Avto

        self.cursor.execute(
            """SELECT *    
                FROM penalties
                ORDER BY penalties_id;"""
        )
        conn.commit()
        row = self.cursor.fetchall()

        columns = ["penalties_id", "id_of_rental_fines", "name_of_fine", "amount_of_penalty"]

        self.root.rowconfigure(index=0, weight=1)  #
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        # self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("penalties_id", text="id Штрафа", anchor=W)
        self.tree.heading("id_of_rental_fines", text="id Аренды", anchor=W)
        self.tree.heading("name_of_fine", text="Название штрафа", anchor=W)
        self.tree.heading("amount_of_penalty", text="Сумма штрафа", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=75)
        self.tree.column("#2", stretch=NO, width=80)
        self.tree.column("#3", stretch=NO, width=120)
        self.tree.column("#4", stretch=NO, width=100)

        for person in row:
            self.tree.insert("", END, values=person)

        self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def Table4(self):
        self.Table = 'client'

        self.cursor.execute(
            """SELECT  client_id,name,surname,patronymic,phone,city
                FROM client
                ORDER BY client_id;"""
        )
        conn.commit()
        row = self.cursor.fetchall()

        columns = ["client_id", "name", "surname", "patronymic", "phone", "city"]

        self.root.rowconfigure(index=0, weight=1)
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        # self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("client_id", text="id Клиетна", anchor=W)
        self.tree.heading("name", text="Имя", anchor=W)
        self.tree.heading("surname", text="Фамилия", anchor=W)
        self.tree.heading("patronymic", text="Отчество", anchor=W)
        self.tree.heading("phone", text="Телефон", anchor=W)
        self.tree.heading("city", text="Город", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=75)
        self.tree.column("#2", stretch=NO, width=60)
        self.tree.column("#3", stretch=NO, width=70)
        self.tree.column("#4", stretch=NO, width=80)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=100)

        for person in row:
            self.tree.insert("", END, values=person)

        self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def Table5(self):
        self.Table = 'employee'

        self.cursor.execute(
            """SELECT employee_id,name,surname,patronymic,phone,city
                FROM employee
                ORDER BY employee_id;"""
        )

        conn.commit()
        row = self.cursor.fetchall()

        columns = ["employee_id", "name", "surname", "patronymic", "phone", "city"]

        self.root.rowconfigure(index=0, weight=1)  #
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("employee_id", text="id Сотрудника", anchor=W)
        self.tree.heading("name", text="Имя", anchor=W)
        self.tree.heading("surname", text="Фамилия", anchor=W)
        self.tree.heading("patronymic", text="Отчество", anchor=W)
        self.tree.heading("phone", text="Телефон", anchor=W)
        self.tree.heading("city", text="Город", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=90)
        self.tree.column("#2", stretch=NO, width=80)
        self.tree.column("#3", stretch=NO, width=80)
        self.tree.column("#4", stretch=NO, width=80)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=100)

        for person in row:
            self.tree.insert("", END, values=person)

        self.scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def Create(self):
        if Table == 'car_rental':
            Create()
        else:
            return

    def Delete(self):
        if Table == 'car_rental':
            Delete()
        else:
            return

class Create:
    def __init__(self):
        self.Table = Table
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.root = tk.Tk()
        self.root.geometry('300x600+650+150')
        self.root.title('Create')
        self.root.config(bg="#dbdbdb")

        self.Create_Label_1 = tk.Label(self.root, text='Напишите id аренды', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_2 = tk.Label(self.root, text='Напишите id клиена', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_3 = tk.Label(self.root, text='Напишите id авто.', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_4 = tk.Label(self.root, text='Напишите id сотрудника', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_5 = tk.Label(self.root, text='Напишите дату выдачи авто.', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_6 = tk.Label(self.root, text='Напишите количество дней', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_7 = tk.Label(self.root, text='Напишите дата возврата авто.', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_8 = tk.Label(self.root, text='Напишите id скидки', font=("times new roman", 12),
                                           bg="#dbdbdb")
        self.Create_Label_9 = tk.Label(self.root, text='Напишите id штрафов', font=("times new roman", 12),
                                           bg="#dbdbdb")

        self.Create_Label_1.place(x=50, y=50)
        self.Create_Label_2.place(x=50, y=100)
        self.Create_Label_3.place(x=50, y=150)
        self.Create_Label_4.place(x=50, y=200)
        self.Create_Label_5.place(x=50, y=250)
        self.Create_Label_6.place(x=50, y=300)
        self.Create_Label_7.place(x=50, y=350)
        self.Create_Label_8.place(x=50, y=400)
        self.Create_Label_9.place(x=50, y=450)

        self.Create_Entry_1 = tk.Entry(self.root)
        self.Create_Entry_2 = tk.Entry(self.root)
        self.Create_Entry_3 = tk.Entry(self.root)
        self.Create_Entry_4 = tk.Entry(self.root)
        self.Create_Entry_5 = tk.Entry(self.root)
        self.Create_Entry_6 = tk.Entry(self.root)
        self.Create_Entry_7 = tk.Entry(self.root)
        self.Create_Entry_8 = tk.Entry(self.root)
        self.Create_Entry_9 = tk.Entry(self.root)

        self.Create_Entry_1.place(x=70, y=80)
        self.Create_Entry_2.place(x=70, y=130)
        self.Create_Entry_3.place(x=70, y=180)
        self.Create_Entry_4.place(x=70, y=230)
        self.Create_Entry_5.place(x=70, y=280)
        self.Create_Entry_6.place(x=70, y=330)
        self.Create_Entry_7.place(x=70, y=380)
        self.Create_Entry_8.place(x=70, y=430)
        self.Create_Entry_9.place(x=70, y=480)

        self.Search_Button = tk.Button(self.root, text='Create', command=self.Create_Button)
        self.Search_Button.place(x=80, y=550)

    def Create_Button(self):
        try:
            Table = self.Table
            Create_1 = self.Create_Entry_1.get()
            Create_2 = self.Create_Entry_2.get()
            Create_3 = self.Create_Entry_3.get()
            Create_4 = self.Create_Entry_4.get()
            Create_5 = self.Create_Entry_5.get()
            Create_6 = self.Create_Entry_6.get()
            Create_7 = self.Create_Entry_7.get()
            Create_8 = self.Create_Entry_8.get()
            Create_9 = self.Create_Entry_9.get()

            self.Create_Entry_1.delete(0, 'end')
            self.Create_Entry_2.delete(0, 'end')
            self.Create_Entry_3.delete(0, 'end')
            self.Create_Entry_4.delete(0, 'end')
            self.Create_Entry_5.delete(0, 'end')
            self.Create_Entry_6.delete(0, 'end')
            self.Create_Entry_7.delete(0, 'end')
            self.Create_Entry_8.delete(0, 'end')
            self.Create_Entry_9.delete(0, 'end')

            self.cursor.execute(
                """CALL inset_python_car_r(%s,%s,%s,%s,date'%s',smallint '%s',date'%s',%s,%s);""" %(Create_1,
                                                                            Create_2,Create_3,Create_4, Create_5,
                                                                            Create_6,Create_7, Create_8, Create_9)
            )
            conn.commit()
        except Exception as _ex:
            messagebox.showwarning(title='Error', message=[_ex])
            self.root.destroy()
        else:
            self.root.destroy()

class Delete:
    def __init__(self):
        self.Table = Table
        self.conn = conn
        self.cursor = self.conn.cursor()

        self.root = tk.Tk()
        self.root.geometry('300x300+650+300')
        self.root.title('Create')
        self.root.config(bg="#dbdbdb")

        self.Delete_Label = tk.Label(self.root, text='Напишите id для удаления', font=("times new roman", 12),
                                       bg="#dbdbdb")
        self.Delete_Label.place(x=60, y=90)

        self.Delete_Entry = tk.Entry(self.root)
        self.Delete_Entry.place(x=80, y=120)

        self.Delete_Button = tk.Button(self.root, text='Delete',command=self.Delete_Button )
        self.Delete_Button.place(x=120, y=150)

        self.root.mainloop()

    def Delete_Button(self):
        try:
            Delete_1 = self.Delete_Entry.get()

            self.Delete_Entry.delete(0, 'end')

            self.cursor.execute(
                """CALL delete_python_car_r(%s);""" %Delete_1
            )
            conn.commit()
        except Exception as _ex:
            messagebox.showwarning(title='Error', message=[_ex])
            self.root.destroy()
        else:
            self.root.destroy()

LoginView()

