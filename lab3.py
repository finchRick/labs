import sys
import os
import logging
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton,
    QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
)
from PySide6.QtCore import Qt
from datetime import datetime

logging.basicConfig(filename='errors.log', level=logging.WARNING, encoding='utf-8')
logger = logging.getLogger(__name__)

class Income:
    def __init__(self, source, money, date):
        self.source = source
        self.money = money
        self.date = date

    def to_row(self):
        return [self.source, str(self.money), self.date]

    def to_file_string(self):
        raise NotImplementedError

class Salary(Income):
    def __init__(self, source, money, firm, date):
        super().__init__(source, money, date)
        self.firm = firm

    def to_row(self):
        return ["Salary", self.source, str(self.money), f"Firm: {self.firm}", self.date]

    def to_file_string(self):
        return f"Salary {self.source} {self.money} {self.firm} {self.date}"

class Rent(Income):
    def __init__(self, source, money, tenant, date):
        super().__init__(source, money, date)
        self.tenant = tenant

    def to_row(self):
        return ["Rent", self.source, str(self.money), f"Tenant: {self.tenant}", self.date]

    def to_file_string(self):
        return f"Rent {self.source} {self.money} {self.tenant} {self.date}"

class IncomeManager:
    def __init__(self):
        self.records = []

    def add(self, record):
        self.records.append(record)

    def delete(self, index):
        if 0 <= index < len(self.records):
            del self.records[index]

    def load_from_file(self, filename):
        self.records.clear()
        if not os.path.exists(filename):
            return
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                try:
                    record = self.parse_line(line)
                    self.records.append(record)
                except Exception as e:
                    logger.warning(f"Line {line_num}: {line.strip()} - {e}")

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for record in self.records:
                f.write(record.to_file_string() + "\n")

    @staticmethod
    def parse_line(line):
        parts = line.strip().split()
        if not parts:
            raise ValueError("Пустая строка")

        type_ = parts[0]
        try:
            if type_ == "Rent" and len(parts) == 5:
                source, money, tenant, date = parts[1], int(parts[2]), parts[3], parts[4]
            elif type_ == "Salary" and len(parts) == 5:
                source, money, firm, date = parts[1], int(parts[2]), parts[3], parts[4]
            else:
                raise ValueError(f"Неверный формат: {line.strip()}")

            try:
                datetime.strptime(date, "%d.%m.%Y")
            except ValueError:
                raise ValueError(f"Неверный формат даты: {date} (ожидается ДД.ММ.ГГГГ)")

            if type_ == "Rent":
                return Rent(source, money, tenant, date)
            else:
                return Salary(source, money, firm, date)
        except Exception as e:
            raise ValueError(f"Ошибка при разборе строки: {e}")

class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Record")
        layout = QFormLayout(self)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Rent", "Salary"])
        layout.addRow("Type:", self.type_combo)

        self.source_input = QLineEdit()
        layout.addRow("Source:", self.source_input)

        self.money_input = QLineEdit()
        layout.addRow("Money:", self.money_input)

        self.tenant_input = QLineEdit()
        layout.addRow("Tenant (for Rent):", self.tenant_input)

        self.firm_input = QLineEdit()
        layout.addRow("Firm (for Salary):", self.firm_input)

        self.date_input = QLineEdit()
        layout.addRow("Date (DD.MM.YYYY):", self.date_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_data(self):
        type_ = self.type_combo.currentText()
        source = self.source_input.text()
        try:
            money = int(self.money_input.text())
        except ValueError:
            raise ValueError("Money must be an integer")
        date = self.date_input.text()

        if type_ == "Rent":
            tenant = self.tenant_input.text()
            return Rent(source, money, tenant, date)
        else:
            firm = self.firm_input.text()
            return Salary(source, money, firm, date)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Income Manager")
        self.setGeometry(100, 100, 800, 600)

        self.manager = IncomeManager()
        self.manager.load_from_file("inp.txt")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "Source", "Money", "Details", "Date"])
        self.update_table()
        self.layout.addWidget(self.table)

        self.add_button = QPushButton("Add Record")
        self.add_button.clicked.connect(self.add_record)
        self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_record)
        self.layout.addWidget(self.delete_button)

    def update_table(self):
        self.table.setRowCount(len(self.manager.records))
        for row, record in enumerate(self.manager.records):
            for col, value in enumerate(record.to_row()):
                self.table.setItem(row, col, QTableWidgetItem(value))
        self.table.resizeColumnsToContents()

    def add_record(self):
        dialog = AddRecordDialog(self)
        if dialog.exec():
            try:
                record = dialog.get_data()
                self.manager.add(record)
                self.update_table()
                self.manager.save_to_file("inp.txt")
            except Exception as e:
                logger.warning(f"Error adding record: {e}")

    def delete_record(self):
        selected = self.table.selectedIndexes()
        if selected:
            row = selected[0].row()
            self.manager.delete(row)
            self.update_table()
            self.manager.save_to_file("inp.txt")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
