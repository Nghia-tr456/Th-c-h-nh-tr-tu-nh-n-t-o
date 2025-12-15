# THỰC HÀNH MÔN TRÍ TUỆ NHÂN TẠO

Repository này lưu trữ mã nguồn 3 bài toán kinh điển trong AI, được cài đặt bằng Python với giao diện trực quan (Matplotlib), hỗ trợ Input động và tối ưu thuật toán.

## Yêu cầu cài đặt (Requirements)
Để chạy được các chương trình, cần cài đặt thư viện đồ họa và tính toán:
pip install matplotlib numpy

1. 8-Puzzle Solver
file: Akt.py
Giải quyết bài toán trượt số 8 ô để về trạng thái đích.
Thuật toán: Akt.
Tính năng:
+ Cho phép nhập trạng thái bắt đầu tùy ý.
+ Tối ưu: Sử dụng kỹ thuật Truy vết (Backtracking) để chỉ vẽ ra đường đi lời giải đúng nhất.
+ Giao diện: Hiển thị trực quan từng bước di chuyển kèm chỉ số g, h, f.

2. Bài toán Cờ Caro (Tic-Tac-Toe)
File: Doikhang_Final.py
Game cờ Caro đối kháng giữa Người và Máy.
Thuật toán: Minimax kết hợp cắt tỉa Alpha-Beta (Alpha-Beta Pruning).
Tính năng:
+ Dynamic Input: Tùy chọn kích thước bàn cờ (3x3, 4x4, 5x5...).
+ Hiệu năng: Cắt tỉa nhánh giúp AI tính toán nhanh, không bị treo ở bàn cờ lớn.
+ Cấu trúc: Code phân chia rõ ràng Class Game và Class AI.

3. Bài toán Tô màu đồ thị (Graph Coloring)
File: Tomau_Final.py
Chương trình tô màu các đỉnh đồ thị sao cho 2 đỉnh kề nhau khác màu.
Thuật toán: Greedy Coloring (Tô màu tham lam).
Tính năng:
+ Random Graph: Tự động sinh đồ thị ngẫu nhiên theo số lượng đỉnh người dùng nhập.
+ Animation: Mô phỏng từng bước quá trình tô màu (Duyệt đỉnh -> Chọn màu -> Tô).

+ Layout: Sắp xếp đỉnh theo hình tròn dễ quan sát.
