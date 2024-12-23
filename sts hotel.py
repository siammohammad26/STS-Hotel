class BookingError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = {"single": {"total": 10, "price": 100},"double": {"total": 8, "price": 150},"suite": {"total": 5, "price": 300}}

    def show_rooms(self):
        print(f"\nRooms available in {self.name}:")
        for room_type, details in self.rooms.items():
            print(f"{room_type.capitalize()}: {details['total']} rooms at ${details['price']} per night")
    def calculate_total_cost(self,nights, room_type):
        if room_type == "single":
             return (100*nights)-((100*nights)*(10/100))
        if room_type == "double":
            return (150*nights)-((150*nights)*(15/100))
        else:
            return (300*nights)-((300*nights)*(20/100))


class Booking(Hotel):
    def __init__(self, name):
        super().__init__(name)
        self.bookings = []

    def book_room(self, customer_name, room_type, nights, discount=None):
        if room_type not in self.rooms:
            raise BookingError("Invalid room type!")
        if self.rooms[room_type]["total"] == 0:
            raise BookingError(f"No {room_type} rooms available!")

        total_cost = self.rooms[room_type]["price"] * nights
        total_cost = calculate_discount(total_cost, discount)
        self.bookings.append({"name": customer_name.title(),"room_type": room_type,"nights": nights,"cost": total_cost,})
        self.rooms[room_type]["total"] -= 1
        print(f"Booking confirmed for {customer_name.title()}! Total cost: ${total_cost:.2f}")

    def view_bookings(self):
        if not self.bookings:
            print("\nNo bookings found.")
            return

        print("\nCurrent bookings:")
        for i, booking in enumerate(self.bookings, 1):
            print(
                f"{i}. {booking['name']} - {booking['room_type'].capitalize()} for {booking['nights']} night(s), Total: ${booking['cost']:.2f}")

    def cancel_booking(self, customer_name, room_type):
        for booking in self.bookings:
            if booking['name'].lower() == customer_name.lower() and booking['room_type'] == room_type:
                self.bookings.remove(booking)
                self.rooms[room_type]["total"] += 1
                print(f"Booking for {customer_name.title()} in a {room_type} room has been canceled.")
                return
        print(f"No booking found for {customer_name.title()} in a {room_type} room.")


class Payment:
    def make_payment(self, amount):
        print(f"\nProcessing payment of ${amount}...")


class CreditCardPayment(Payment):
    def make_payment(self, amount):
        print(f"Payment of ${amount} made using Credit Card.")


class BkashPayment(Payment):
    def make_payment(self, amount):
        print(f"Payment of ${amount} made using Bkash.")


def calculate_discount(cost, discount=None):
    if discount is None:
        return cost
    elif isinstance(discount, (int, float)):
        return cost - (cost * (discount / 100))
    else:
        raise ValueError("Invalid discount type. Provide a number.")


class HotelUtility(Booking):
    def __init__(self, name):
        super().__init__(name)
        self.users = {"admin": {"password": "admin123", "role": "admin"}}
        self.current_user = None

    def signup(self, username, password, role):
        if username in self.users:
            print("Username already exists. Please log in.")
            return
        self.users[username] = {"password": password, "role": role}
        print(f"User {username} signed up successfully!")

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = {"username": username, "role": self.users[username]["role"]}
            print(f"Welcome, {username}!")
        else:
            print("Invalid username or password.")

    def logout(self):
        self.current_user = None
        print("Logged out successfully!")


def main():
    hotel = HotelUtility("Grand STS Hotel")
    payment_methods = {"1": CreditCardPayment(), "2": BkashPayment()}
    discounts = {"single": 10, "double": 15, "suite": 20}  # Discount percentages per room type

    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. Show Rooms")
        print("4. Book Room")
        print("5. View Bookings")
        print("6. Cancel Booking")
        print("7. Logout")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            role = input("Enter role (admin/customer): ").strip().lower()
            hotel.signup(username, password, role)

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            hotel.login(username, password)

        elif choice == "3":
            hotel.show_rooms()

        elif choice == "4":
            if hotel.current_user and hotel.current_user["role"] == "customer":
                try:
                    customer_name = hotel.current_user["username"]
                    room_type = input("Enter room type (single/double/suite): ").strip().lower()
                    nights = int(input("Enter number of nights: "))
                    discount = discounts.get(room_type, None)
                    hotel.book_room(customer_name, room_type, nights, discount)
                    payment_choice = input("\nChoose Payment Method (1: Credit Card, 2: Bkash): ").strip()
                    if payment_choice in payment_methods:
                        payment_methods[payment_choice].make_payment(hotel.calculate_total_cost(nights, room_type))
                    else:
                        print("Invalid payment method. Skipping payment.")
                except BookingError as e:
                    print(f"Error: {e}")
                except ValueError:
                    print("Invalid input. Please try again.")
            else:
                print("You must be logged in as a customer to book a room.")

        elif choice == "5":
            hotel.view_bookings()

        elif choice == "6":
            if hotel.current_user and hotel.current_user["role"] == "customer":
                customer_name = hotel.current_user["username"]
                room_type = input("Enter room type to cancel (single/double/suite): ").strip().lower()
                hotel.cancel_booking(customer_name, room_type)
            else:
                print("You must be logged in as a customer to cancel a booking.")

        elif choice == "7":
            hotel.logout()

        elif choice == "8":
            print("Thank you for visiting Grand STS Hotel. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()