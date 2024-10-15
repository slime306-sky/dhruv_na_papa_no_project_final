import sqlite3 as sql

class data_manager:

    def __init__(self) -> None:
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id VARCHAR(100) NOT NULL,
                "no" INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                name VARCHAR(255) NOT NULL,
                box INTEGER NOT NULL,
                dozen INTEGER,
                total_items INTEGER,
                weight DECIMAL(10, 2),
                total_weight DECIMAL(10, 2),
                price DECIMAL(5, 2),
                total_price DECIMAL(10, 5),
                flag INTEGER
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company (
                "no" INTEGER PRIMARY KEY,
                company_name VARCHAR(50) NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

    def calculatePaisaUsingTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, total_item: int, option_input: float, company: str):
        total_paisa = int(total_item) * int(option_input)
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_paisa, 1))

    def calculatePaisausingDozenTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, company: str):
        total_item = dazon * 12
        total_paisa = total_item * float(option_input)

        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_paisa, 1))

    def calculatePaisaUsingDozen(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, company: str):
        total_paisa = int(dazon) * float(option_input)
        total_item = int(dazon) * 12
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_paisa, 0))

    def calculateWieghtUsingDozenToTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, company: str):
        total_item = dazon * 12
        total_weight = total_item * float(option_input)

        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_weight, 1))

    def calculateBothUsingDozenTOTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, both: float, company: str):
        total_item = dazon * 12
        total_paisa = total_item * float(option_input)
        total_weight = total_item * float(both)
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, both, total_weight, option_input, total_paisa, 1))

    def calculateBothUsingTotalitem(self, cursor, date: str, name: str, box: int, dazon: int, total_item: int, option_input: float, both: float, company: str):
        total_paisa = int(total_item) * float(option_input)
        total_weight = int(total_item) * float(both)
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, both, total_weight, option_input, total_paisa, 1))

    def calculateBothUsingdozen(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, both: float, company: str):
        total_paisa = int(dazon) * float(option_input)
        total_item = int(dazon) * 12
        total_weight = total_item * float(both)
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, both, total_weight, option_input, total_paisa, 0))

    def add_data(self, date: str, name: str, box: int, total_item: int, option_input: float, option: str, count: str, both: str, company: str):
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        try:
            box = int(box)
            option_input = float(option_input)
        except ValueError:
            total_item = None

        dazon = box * 6

        if both == "":
            if option == "paisa":
                if count == "on":
                    self.calculatePaisaUsingDozen(self,cursor, date, name, box, dazon, option_input, company)
                elif count == "off":
                    self.calculatePaisaUsingDozen(self,cursor, date, name, box, dazon, option_input, company)
            elif option == "weight":
                self.calculateWieghtUsingDozenToTotalItem(self,cursor, date, name, box, dazon, option_input, company)
        else:
            if option == "paisa":
                if count == "on":
                    self.calculateBothUsingdozen(self,cursor, date, name, box, dazon, option_input, both, company)
                elif count == "off":
                    self.calculateBothUsingdozen(self,cursor, date, name, box, dazon, option_input, both, company)
            elif option == "weight":
                self.calculateBothUsingDozenTOTotalItem(self,cursor, date, name, box, dazon, option_input, both, company)

        conn.commit()
        conn.close()

    def get_company_data(self, selection: str, company: str):
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        
        # Fetch data based on selection and company
        if selection == 'paisa':
            cursor.execute("SELECT no,date, name, box, dozen, total_items, price, total_price, flag FROM data WHERE id = ?", (company,))
        elif selection == 'weight':
            cursor.execute("SELECT no,date, name, box, dozen, total_items, weight, total_weight, flag FROM data WHERE id = ?", (company,))
        
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_data(self):
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT no, company_name FROM company")
        rows = cursor.fetchall()
        conn.close()
        return rows
