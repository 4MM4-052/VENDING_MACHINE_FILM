Giao diện của ứng dụng, phát triển trên nền tảng Tkinter, cho phép người dùng thực hiện các thao tác mua vé nhanh chóng và dễ dàng. Đồng thời, việc tích hợp cơ sở dữ liệu SQLite không chỉ giúp lưu trữ thông tin an toàn mà còn đảm bảo khả năng quản lý dữ liệu hiệu quả thông qua lịch sử giao dịch.
Hệ thống máy bán vé có thể được biểu diễn bằng Finite Automata với:
- Tập hợp trạng thái (Q):
  + waiting_for_selection: Máy đang chờ người dùng chọn vé.
  + ticket_selected: Người dùng đã chọn một vé.
  + payment: Người dùng thực hiện thanh toán.
  + printing: Máy đang in vé.
  + complete: Quá trình giao dịch hoàn tất.

- Hàm chuyển trạng thái (δ) Dựa trên trạng thái hiện tại và hành động của người dùng (input), máy sẽ chuyển sang trạng thái mới.
-	Tập hợp đầu vào (Σ):
    +	select_ticket: Chọn vé.
    + make_payment: Thanh toán.
    + print_ticket: In vé.
    + finish: Hoàn tất giao dịch.
    + reset: Khởi tạo lại giao dịch.

- Trạng thái bắt đầu (q₀): waiting_for_selection.
- Tập hợp trạng thái kết thúc (F): complete.
- Cấu trúc chính của hệ thống:
  
  ![image](https://github.com/user-attachments/assets/6f69d3bd-0127-4ebc-abc7-61fa86f8cba1)

Sơ đồ chuyển DFA của mô hình

  ![image](https://github.com/user-attachments/assets/1585f8c8-6568-4cc3-86b6-5d83b437a24c)

  
Giao diện người dùng

   ![image](https://github.com/user-attachments/assets/e4b429bb-2ba9-4022-b785-bd7a5f63a723)


Chọn loại vé:

  ![image](https://github.com/user-attachments/assets/6e3738c5-2bcd-4339-8766-5cf09a7636b5)

Giao diện danh sách phim

![image](https://github.com/user-attachments/assets/8c719fd9-fc25-44c3-893c-fa2cd6aa5c6e)

![image](https://github.com/user-attachments/assets/fe0bb71f-1e7a-4a42-ae4e-72ec7445ce4b)


Chọn phương thức thanh toán: 

   ![image](https://github.com/user-attachments/assets/a9c93d48-67eb-4fa9-885b-49088566b372)


In vé:

  ![image](https://github.com/user-attachments/assets/50f2d5d5-1ac3-43bc-8f2b-caccd676da2c)

Lịch sử giao dịch

  ![image](https://github.com/user-attachments/assets/f0b5f830-d912-4943-9f6a-528ae9bc33db)
