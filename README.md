# 🤖 Hotel & Restaurant Management Chatbots

A powerful dual-bot system featuring a Hotel Booking Assistant and Restaurant Order Manager trainned with organic Dataset. Built with Python and MySQL for seamless automation of hospitality services.

## 🌟 Features

### 🏨 Hotel Booking Bot
- 📝 Process new room bookings
- 🔍 Check room availability in real-time
- 💾 Store booking information in MySQL database
- 🔄 Update room status automatically

### 🍽️ Restaurant Order Bot
- 🛒 Take new food orders
- 📋 Manage menu items
- 💳 Process order details
- 📦 Store order history in MySQL database

## 🛠️ Tech Stack
- 📍 Python 3.8+
- 🗄️ MySQL Database
- 🔌 mysql-connector-python
- 🤖 Python's built-in libraries

## 📋 Prerequisites
- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)
- Basic knowledge of SQL queries

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hotel-restaurant-bots.git
cd hotel-restaurant-bots
```



### 2. Database Setup
```sql
-- Create the hotel_bookings table
CREATE TABLE hotel_bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_name VARCHAR(100),
    room_number INT,
    check_in DATE,
    check_out DATE,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the restaurant_orders table
CREATE TABLE restaurant_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    items JSON,
    total_amount DECIMAL(10,2),
    order_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Environment Setup
Replace email password with your gmail SMTP to send email alert after booking.

### 5. Run the Bots
```bash
# For Hotel Booking Bot
python bot.py

# For Restaurant Order Bot
python bot2.py
```

## 💻 Usage

### Hotel Booking Bot
```python
# Example interaction with Hotel Bot
python bot.py

# Bot commands:
/book - Book a new room
/availability - Check available rooms
/status - Check booking status
/help - Show all commands
```

### Restaurant Order Bot
```python
# Example interaction with Restaurant Bot
python bot2.py

# Example commands:
/menu - Show menu items
/order - Place new order
/status - Check order status
/help - Show all commands
```

> But you can chat normally, the bot will understand as it is trainned with real dataset.

## 📊 Database Schema

### Hotel Bookings Table
| Column | Type | Description |
|--------|------|-------------|
| booking_id | INT | Primary Key |
| guest_name | VARCHAR(100) | Guest's full name |
| room_number | INT | Assigned room number |
| check_in | DATE | Check-in date |
| check_out | DATE | Check-out date |
| status | VARCHAR(20) | Booking status |
| created_at | TIMESTAMP | Booking creation time |

### Restaurant Orders Table
| Column | Type | Description |
|--------|------|-------------|
| order_id | INT | Primary Key |
| customer_name | VARCHAR(100) | Customer's name |
| items | JSON | Ordered items details |
| total_amount | DECIMAL | Order total |
| order_status | VARCHAR(20) | Order status |
| created_at | TIMESTAMP | Order creation time |

## 🔧 Configuration
Both bots can be configured through their respective config files:
- `config/hotel_config.py`
- `config/restaurant_config.py`

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support
For support:
- 📧 Email: tanvir.rrrabin@gmail.com
- 💬 Create an issue
- 📚 Check documentation

## ⭐ Show your support
Give a ⭐️ if this project helped you!

---
Made with ❤️ by Robin | © 2024 All rights reserved
