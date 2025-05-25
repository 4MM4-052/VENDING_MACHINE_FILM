import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Thêm import cho Treeview
from PIL import Image, ImageTk
import sqlite3
import datetime

class TicketMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máy Bán Vé Xem Phim")
        self.root.configure(bg='white')

        # Background image (optional)
        self.background_image = Image.open("./image/background.jpg").resize(
            (root.winfo_screenwidth(), root.winfo_screenheight()))
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        bg_label = tk.Label(self.root, image=self.background_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.state("zoomed")
        self.machine = TicketMachine()

        # Title Label
        title_label = tk.Label(self.root, text="Máy Bán Vé Xem Phim", font=("Times New Roman", 36, 'bold'), bg='lightgray',
                               pady=20)
        title_label.pack()

        # Status Label
        self.status_label = tk.Label(self.root, text="Trạng thái: Chờ lựa chọn loại vé", font=("Times New Roman", 20),
                                     bg='lightgray')
        self.status_label.pack(pady=10)

        # History Button
        history_button = tk.Button(self.root, text="Xem Lịch sử Giao dịch", command=self.show_history, bg='lightgreen',
                                   font=("Times New Roman", 16))
        history_button.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.root, bg='lightblue')
        button_frame.pack(pady=20)

        # Buttons
        self.create_button(button_frame, "Chọn loại vé", self.select_ticket_type)
        self.create_button(button_frame, "Thanh toán", self.select_payment_method)
        self.create_button(button_frame, "In vé", self.print_ticket)
        self.create_button(button_frame, "Hoàn tất", self.finish)
        self.create_button(button_frame, "Khởi tạo lại", self.reset)

        # # Footer
        # footer_frame = tk.Frame(self.root, bg='lightgray')
        # footer_frame.pack(side="bottom", fill="x", pady=5)
        #
        # footer_label = tk.Label(footer_frame, text="© 2024 Máy Bán Vé, Tất cả quyền được bảo lưu.", font=("Times New Roman", 10),
        #                         bg='lightgray')
        # footer_label.pack()

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, width=25, height=2, command=command, bg='skyblue', font=("Times New Roman", 16),
                           borderwidth=2, relief='raised')
        button.pack(side='top', pady=10, padx=10, fill='x')

        # Adding hover effect
        button.bind("<Enter>", lambda e: button.config(bg='deepskyblue'))
        button.bind("<Leave>", lambda e: button.config(bg='skyblue'))

    def update_status(self):
        self.status_label.config(text=f"Trạng thái: {self.machine.current_state.capitalize()}")

    def select_ticket_type(self):
        type_window = tk.Toplevel(self.root)
        type_window.title("Chọn loại vé")
        type_window.geometry("400x200")
        type_window.configure(bg='white')

        # Buttons for ticket types
        tk.Button(type_window, text="Vé bình thường", width=20,
                  command=lambda: self.show_tickets("Vé bình thường", type_window), bg='lightgreen',
                  font=("Times New Roman", 14)).pack(pady=10)
        tk.Button(type_window, text="Vé VIP", width=20,
                  command=lambda: self.show_tickets("Vé VIP", type_window), bg='lightgreen', font=("Times New Roman", 14)).pack(
            pady=10)

    def show_tickets(self, ticket_type, type_window):
        type_window.destroy()
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title(f"Chọn {ticket_type}")
        # Tạo canvas và khung để cuộn
        ticket_window.state("zoomed")
        self.canvas = tk.Canvas(ticket_window)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(ticket_window, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Tạo khung để giữ tất cả các nút vé
        self.frame = tk.Frame(self.canvas)
        # Tạo cửa sổ trên canvas để giữ khung
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        # Liên kết sự kiện cấu hình để cập nhật vùng có thể cuộn khi kích thước khung hình thay đổi
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: canvas.config(scrollregion=canvas.bbox("all")))

        # Ticket data
        self.tickets = {
            "Vé bình thường": [
                {"name": "Zootopi", "image": "./image/img_5.png"},
                {"name": "Kung Fu Panda 4", "image": "./image/img_17.jpg"},
                {"name": "Chú Gấu Vivo", "image": "./image/img_27.jpg"},
                {"name": "Rap Phờ Đập Phá", "image": "./image/img_28.jpg"},
                {"name": "Chú Mèo Đi Lạc", "image": "./image/img_29.jpg"},
                {"name": "Chuột Nhí Và Sứ Mệnh Thần Biển", "image": "./image/img_18.jpg"},
                {"name": "Anh Em Super Mario", "image": "./image/img_19.png"},
                {"name": "Mèo Béo Siêu Đẳng", "image": "./image/img_20.jpg"},
                {"name": "Happy Feet", "image": "./image/img_6.png"},
                {"name": "Tangled", "image": "./image/img_8.png"},
                {"name": "Turning Red", "image": "./image/img_9.png"},
                {"name": "The Little Mermaid", "image": "./image/img_10.png"},
                {"name": "Minions-Sự Trỗi Dậy Của Gru", "image": "./image/img_12.png"},
                {"name": "Mùa Hè Của Luca", "image": "./image/img_14.png"},
                {"name": "Oscar's Oasis", "image": "./image/img_15.png"},
                {"name": "Snow White And The Seven Dwarfs", "image": "./image/img_16.png"}
            ],
            "Vé VIP": [
                {"name": "Thỏ Gà Rà Và Kho Báu", "image": "./image/img_1.jpg"},
                {"name": "Evangelion: 1.0 You Are (not) Alone", "image": "./image/img_27.png"},
                {"name": "Evangelion: 2.22 You Can (not) Advance", "image": "./image/img_28.png"},
                {"name": "Biệt Đội Hải Cẩu", "image": "./image/img_23.jpg"},
                {"name": "Trở Lại Vùng Hoang Dã", "image": "./image/img_24.jpg"},
                {"name": "Chim Cổ Đỏ Robin", "image": "./image/img_25.jpg"},
                {"name": "Tế Công: Hàng Long Giáng Thế", "image": "./image/img_26.jpg"},
                {"name": "Nhím Sonic", "image": "./image/img_21.jpg"},
                {"name": "Tây Du Ký: Tái chiến ma vương", "image": "./image/img_22.jpg"},
                {"name": "Ozi: Phi Vụ Rừng Xanh", "image": "./image/img_16.jpg"},
                {"name": "WALL-E", "image": "./image/img_2.png"},
                {"name": "Raya And The Last Dragon", "image": "./image/img_3.png"},
                {"name": "Peter Pan", "image": "./image/img_4.png"},
                {"name": "DC-Liên Minh Siêu Thú", "image": "./image/img_7.png"},
                {"name": "Pororo-Dragon Castle Adventure", "image": "./image/img_11.png"},
                {"name": "Con Rồng Cháu Tiên", "image": "./image/img_13.png"}
            ],
        }

        row = 0
        col = 0
        for ticket in self.tickets[ticket_type]:
            try:
                img = Image.open(ticket["image"]).resize((370, 340))
                photo = ImageTk.PhotoImage(img)
                btn = tk.Button(self.frame, image=photo, text=ticket["name"], compound="top",
                                command=lambda t=ticket: self.choose_ticket(t, ticket_window), bg='lightblue',
                                font=("Times New Roman", 14, 'bold'))
                btn.image = photo  # Prevent garbage collection
                btn.grid(row=row, column=col, sticky="nsew")
                col += 1
                if col > 3:  # After 4 columns, move to the next row
                    col = 0
                    row += 1
            except FileNotFoundError:
                print(f"Hình ảnh {ticket['image']} không tìm thấy.")
                continue  # Skip this ticket and move to the next one
        # Đảm bảo khung vẽ sẽ cuộn để vừa với tất cả nội dung
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        # Liên kết sự kiện bánh xe chuột để cuộn
        ticket_window.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def choose_ticket(self, ticket, window):
        """Lựa chọn vé và cập nhật trạng thái."""
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn chọn vé '{ticket['name']}' không?"):
            result = self.machine.select_ticket(ticket)
            messagebox.showinfo("Thông báo", result)
            self.update_status()
            window.destroy()

    def select_payment_method(self):
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Chọn phương thức thanh toán")
        payment_window.geometry("400x200")
        payment_window.configure(bg='white')

        # Payment method buttons
        cash_button = tk.Button(payment_window, text="Thanh toán bằng Tiền mặt", width=24,
                                command=lambda: self.make_payment("Tiền mặt", payment_window), bg='lightgreen',
                                font=("Times New Roman", 14))
        cash_button.pack(pady=10)

        credit_button = tk.Button(payment_window, text="Thanh toán bằng Thẻ tín dụng", width=24,
                                  command=lambda: self.make_payment("Thẻ tín dụng", payment_window), bg='lightgreen',
                                  font=("Times New Roman", 14))
        credit_button.pack(pady=10)

        ewallet_button = tk.Button(payment_window, text="Thanh toán bằng Ví điện tử", width=24,
                                   command=lambda: self.make_payment("Ví điện tử", payment_window), bg='lightgreen',
                                   font=("Times New Roman", 14))
        ewallet_button.pack(pady=10)

    def make_payment(self, payment_method, payment_window):
        """Tiến hành thanh toán."""
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn thanh toán bằng {payment_method} không?"):
            result = self.machine.make_payment(payment_method)
            messagebox.showinfo("Thông báo", result)
            self.update_status()
            payment_window.destroy()

    def print_ticket(self):
        """In vé."""
        result = self.machine.print_ticket()
        messagebox.showinfo("Thông báo", result)
        self.update_status()

    def finish(self):
        """Hoàn tất giao dịch."""
        result = self.machine.finish()
        messagebox.showinfo("Thông báo", result)
        self.update_status()

    def reset(self):
        """Khởi tạo lại."""
        result = self.machine.reset()
        messagebox.showinfo("Thông báo", result)
        self.update_status()

    def show_history(self):
        """Hiển thị lịch sử giao dịch."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Lịch sử Giao dịch")
        history_window.geometry("800x400")

        # Tạo Treeview cho lịch sử giao dịch
        self.tree = ttk.Treeview(history_window, columns=("Tên vé", "Phương thức thanh toán", "Thời gian"),
                                 show='headings')
        self.tree.heading("Tên vé", text="Tên vé")
        self.tree.heading("Phương thức thanh toán", text="Phương thức thanh toán")
        self.tree.heading("Thời gian", text="Thời gian")

        # Thay đổi kích thước cột
        self.tree.column("Tên vé", anchor="center")
        self.tree.column("Phương thức thanh toán", anchor="center")
        self.tree.column("Thời gian", anchor="center")

        # Lấy dữ liệu lịch sử giao dịch
        history = self.machine.transaction_history.get_history()
        for tr in history:
            self.tree.insert("", "end", values=tr)
        self.tree.pack(expand=True, fill='both')
        # Tạo Scrollbar cho Treeview
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        # Thêm nút Clear
        clear_button = tk.Button(history_window, text="Clear", command=self.clear_history,
                                 bg='lightcoral',font=("Times New Roman", 13))
        clear_button.pack(pady=10)

    def clear_history(self):
        """Xóa tất cả lịch sử giao dịch trong Treeview và cơ sở dữ liệu."""
        self.machine.transaction_history.clear_all_transactions()  # Xóa tất cả trong cơ sở dữ liệu
        for item in self.tree.get_children():
            self.tree.delete(item)  # Xóa tất cả trong Treeview


# Khởi tạo ứng dụng Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = TicketMachineApp(root)
    root.mainloop()
