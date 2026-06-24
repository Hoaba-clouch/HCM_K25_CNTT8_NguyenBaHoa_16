

class DeliveryOrder:
    def __init__(
        self,
        order_id,
        customer_name,
        delivery_address,
        distance_km,
        cost_per_km,
        package_weight,
        extra_fee,
    ):
        self.id = order_id
        self.customer_name = customer_name
        self.delivery_address = delivery_address
        self.distance_km = distance_km
        self.cost_per_km = cost_per_km
        self.package_weight = package_weight
        self.extra_fee = extra_fee
        self.total_delivery_fee = 0
        self.delivery_type = ""
        self.calculate_delivery_fee()
        self.classify_delivery()
    def calculate_delivery_fee(self):
        self.total_delivery_fee = self.distance_km * self.cost_per_km + self.extra_fee

    def classify_delivery(self):
        if self.total_delivery_fee < 50_000:
            self.delivery_type = "Gần"
        elif self.total_delivery_fee < 150_000:
            self.delivery_type = "Trung bình"
        elif self.total_delivery_fee < 500_000:
            self.delivery_type = "Xa"
        else:
            self.delivery_type = "Rất xa"

    def update_information(
        self, distance_km, cost_per_km, package_weight, extra_fee
    ):
        self.distance_km = distance_km
        self.cost_per_km = cost_per_km
        self.package_weight = package_weight
        self.extra_fee = extra_fee
        self.calculate_delivery_fee()
        self.classify_delivery()
        
        
        

class DeliveryOrderManager:
    def __init__(self):
        self.orders = []
    def find_by_id(self, order_id):
        order_id = order_id.strip().lower()
        for order in self.orders:
            if order.id.lower() == order_id:
                return order
        return None

    def add_order(self):
        order_id = input_non_empty("Nhập mã đơn giao hàng: ")
        if self.find_by_id(order_id):
            print("Mã đơn giao hàng đã tồn tại!")
            return
        customer_name = input_non_empty("Nhập tên khách hàng: ")
        delivery_address = input_non_empty("Nhập địa chỉ giao hàng: ")
        distance_km = input_number(
            "Nhập khoảng cách giao hàng (km): ", allow_zero=False
        )
        cost_per_km = input_number("Nhập đơn giá/km: ")
        package_weight = input_number(
            "Nhập khối lượng kiện hàng (kg): ", allow_zero=False
        )
        extra_fee = input_number("Nhập phụ phí: ")
        order = DeliveryOrder(
            order_id,
            customer_name,
            delivery_address,
            distance_km,
            cost_per_km,
            package_weight,
            extra_fee,
        )
        self.orders.append(order)
        print("Thêm đơn giao hàng thành công!")

    def show_all(self, orders=None):
        displayed_orders = self.orders if orders is None else orders
        if not displayed_orders:
            print("Danh sách đơn giao hàng đang rỗng!")
            return
        print(
            f"{'Mã đơn':<10}{'Khách hàng':<20}{'Địa chỉ':<20}"
            f"{'Km':<8}{'Đơn giá':<12}{'Khối lượng':<12}"
            f"{'Phụ phí':<12}{'Tổng phí':<15}{'Phân loại':<12}"
        )
        print("-" * 121)
        for order in displayed_orders:
            print(
                f"{order.id:<10}{order.customer_name:<20}"
                f"{order.delivery_address:<20}{order.distance_km:<8g}"
                f"{order.cost_per_km:<12,.0f}{order.package_weight:<12g}"
                f"{order.extra_fee:<12,.0f}{order.total_delivery_fee:<15,.0f}"
                f"{order.delivery_type:<12}"
            )

    def update_order(self):
        order_id = input_non_empty("Nhập mã đơn giao hàng cần cập nhật: ")
        order = self.find_by_id(order_id)
        if order is None:
            print("Không tìm thấy đơn giao hàng cần cập nhật!")
            return
        distance_km = input_number("Nhập khoảng cách giao hàng mới (km): ",allow_zero=False,
        )
        cost_per_km = input_number("Nhập đơn giá/km mới: ")
        package_weight = input_number("Nhập khối lượng kiện hàng mới (kg): ",allow_zero=False,
        )
        extra_fee = input_number("Nhập phụ phí mới: ")

        order.update_information(
            distance_km, cost_per_km, package_weight, extra_fee
        )
        print("Cập nhật đơn giao hàng thành công!")
        
        
        
    def delete_order(self):
        order_id = input_non_empty("Nhập mã đơn giao hàng cần xóa: ")
        order = self.find_by_id(order_id)
        if order is None:
            print("Không tìm thấy đơn giao hàng cần xóa!")
            return

        confirmation = input(
            "Bạn có chắc muốn xóa đơn giao hàng này không? (Y/N): "
        ).strip().lower()
        if confirmation == "y":
            self.orders.remove(order)
            print("Xóa đơn giao hàng thành công!")
        elif confirmation == "n":
            print("Đã hủy thao tác xóa.")
        else:
            print("Lựa chọn không hợp lệ!")
            
            
    def search_order(self):
        keyword = input_non_empty(
            "Nhập tên khách hàng hoặc địa chỉ cần tìm: "
        ).lower()
        results = [
            order
            for order in self.orders
            if keyword in order.customer_name.lower()
            or keyword in order.delivery_address.lower()
        ]
        if not results:
            print("Không tìm thấy đơn hàng phù hợp!")
            return
        self.show_all(results)

def input_non_empty(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Thông tin này không được để trống")

def input_number(message, allow_zero=True):
    while True:
        try:
            value = float(input(message))
            if value < 0:
                print("Giá trị không được là số âm")
                continue
            if value == 0 and not allow_zero:
                print("Giá trị phải lớn hơn 0")
                continue
            return value
        except ValueError:
            print("Vui lòng nhập một số hợp lệ!")
manager = DeliveryOrderManager()

while True:
    print("\n================ MENU ================")
    print("1. Hiển thị danh sách đơn giao hàng")
    print("2. Thêm đơn giao hàng mới")
    print("3. Cập nhật đơn giao hàng")
    print("4. Xóa đơn giao hàng")
    print("5. Tìm kiếm đơn giao hàng")
    print("6. Thoát")
    print("======================================")
    choice = input("Nhập lựa chọn của bạn: ").strip()
    match choice:
        case "1":
            manager.show_all()
        case "2":
            manager.add_order()
        case "3":
            manager.update_order()
        case "4":
            manager.delete_order()
        case "5":
            manager.search_order()
        case "6":
            print("Cảm ơn bạn đã sử dụng hệ thống quản lý vận chuyển!")
            break
        case _:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 6!")
