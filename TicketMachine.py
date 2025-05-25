import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Thêm import cho Treeview
from PIL import Image, ImageTk
import sqlite3
import datetime

class TicketMachine:
    def __init__(self):
        self.current_state = "waiting_for_selection"
        self.selected_ticket = None
        self.transaction_history = TransactionHistory()
        self.transaction_time = None  # Thêm biến để lưu thời gian đặt vé
        self.states = {
            "waiting_for_selection": self.waiting_for_selection,
            "ticket_selected": self.ticket_selected,
            "payment": self.payment,
            "printing": self.printing,
            "complete": self.complete
        }

    def waiting_for_selection(self, action):
        if action == 'select_ticket':
            return "ticket_selected"
        return "waiting_for_selection"

    def ticket_selected(self, action):
        if action == 'make_payment':
            return "payment"
        return "ticket_selected"

    def payment(self, action):
        if action == 'print_ticket':
            return "printing"
        return "payment"

    def printing(self, action):
        if action == 'finish':
            return "complete"
        return "printing"

    def complete(self, action):
        if action == 'reset':
            return "waiting_for_selection"
        return "complete"

    def select_ticket(self, ticket):
        if self.current_state == "waiting_for_selection":
            self.selected_ticket = ticket
            transition_action = 'select_ticket'
            self.current_state = self.states[self.current_state](transition_action)
            return f"{ticket['name']} đã được chọn!"
        elif self.current_state == "complete":
            return "Bạn cần khởi tạo lại giao dịch mới!"
        return f"Bạn đã chọn vé {ticket['name']} rồi!"

    def make_payment(self, payment_method):
        if self.current_state == "ticket_selected":
            transition_action = 'make_payment'
            self.payment_method = payment_method  # Lưu phương thức thanh toán
            self.current_state = self.states[self.current_state](transition_action)
            self.transaction_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')  # Lưu thời gian đặt vé
            # Lưu thông tin giao dịch vào lịch sử
            self.transaction_history.add_transaction({
                'name': self.selected_ticket['name'],
                'payment_method': payment_method,
                'transaction_time': self.transaction_time
            })
            return f"Thanh toán bằng {payment_method} thành công!"
        elif self.current_state == "complete":
            return "Bạn cần khởi tạo lại giao dịch mới!"
        elif self.current_state == "waiting_for_selection":
            return "Chưa chọn vé. Vui lòng chọn vé trước!"
        return f"Bạn đã thanh toán bằng {payment_method} rồi!"

    def print_ticket(self):
        if self.current_state == "payment":
            transition_action = 'print_ticket'
            self.current_state = self.states[self.current_state](transition_action)
            self.export_ticket_details()
            return "Đang in vé!"
        elif self.current_state == "printing":
            return "Đang trong quá trình in vé, vui lòng đợi."
        return "Không thể in vé vào lúc này."

    def finish(self):
        if self.current_state == "printing":
            transition_action = 'finish'
            self.current_state = self.states[self.current_state](transition_action)
            return "Giao dịch hoàn tất! Vé đã được in."
        return "Vui lòng in vé trước!"

    def reset(self):
        if self.current_state == "complete":
            transition_action = 'reset'
            self.current_state = self.states[self.current_state](transition_action)
            self.selected_ticket = None
            return "Máy đã sẵn sàng cho giao dịch tiếp theo!"
        return "Không thể quay lại khi chưa hoàn tất giao dịch!"

    def export_ticket_details(self):
        if self.selected_ticket and 'name' in self.selected_ticket:
            # Làm sạch tên vé
            cleaned_name = self.selected_ticket['name'].replace(' ', '_') \
                .replace('/', '_') \
                .replace('\\', '_') \
                .replace(':', '_') \
                .replace('*', '_') \
                .replace('?', '_') \
                .replace('"', '_') \
                .replace('<', '_') \
                .replace('>', '_') \
                .replace('|', '_')

            # Làm sạch thời gian giao dịch
            cleaned_time = self.transaction_time.replace(' ', '_') \
                .replace('/', '_') \
                .replace('\\', '_') \
                .replace(':', '_') \
                .replace('*', '_') \
                .replace('?', '_') \
                .replace('"', '_') \
                .replace('<', '_') \
                .replace('>', '_') \
                .replace('|', '_')

            # Tạo tên file hợp lệ
            filename = f"{cleaned_name}_{cleaned_time}_receipt.txt"

            try:
                # Ghi thông tin vào file
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"--- THÔNG TIN VÉ ---\n")
                    file.write(f"Tên vé: {self.selected_ticket['name']}\n")
                    file.write(f"Thời gian đặt vé: {self.transaction_time}\n")  # Thêm thời gian đặt vé
                    file.write(f"Phương thức thanh toán: {self.payment_method}\n")  # Thêm phương thức thanh toán
                    file.write(f"Trạng thái: Đã thanh toán\n")
                    file.write("Cảm ơn bạn đã đặt vé tại máy bán vé của chúng tôi!\n")
                    file.write("-------------------\n")
                print(f"Đã xuất vé trên {filename}")
            except Exception as e:
                print(f"Đã xảy ra lỗi khi xuất vé: {e}")
        else:
            print("Vé không hợp lệ hoặc chưa được chọn.")

