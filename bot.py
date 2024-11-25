import random
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import training



class HotelChatBot:
    def __init__(self):
        self.context = {}
        self.training_data = self.create_training_data()
        self.vectorizer, self.model = self.train_model()
        self.room_types = {
            "single": {"fare": 100, "prefix": "SN", "total_rooms": 5},
            "double": {"fare": 150, "prefix": "DB", "total_rooms": 5},
            "suite": {"fare": 200, "prefix": "SU", "total_rooms": 5}
        }
        self.state = None

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="hotel_chatbot"
        )
        self.db_cursor = self.db_connection.cursor()

    def create_training_data(self):
        return training.training_data

    def train_model(self):
        X = [text for text, response in self.training_data]
        y = [response for text, response in self.training_data]

        vectorizer = TfidfVectorizer()
        model = LogisticRegression()
        pipeline = make_pipeline(vectorizer, model)
        pipeline.fit(X, y)

        return vectorizer, model

    def count_available_rooms(self):
        """Count the available rooms by subtracting bookings from total rooms."""
        available_rooms = {}
        for room_type in self.room_types:
            query = "SELECT COUNT(*) FROM bookings WHERE room_type = %s"
            self.db_cursor.execute(query, (room_type,))
            booked_count = self.db_cursor.fetchone()[0]
            total_rooms = self.room_types[room_type]["total_rooms"]
            available_rooms[room_type] = total_rooms - booked_count
        return available_rooms

    def show_available_rooms(self):
        """Respond with the available room counts."""
        available_rooms = self.count_available_rooms()
        response = "Here are the available rooms:\n"
        for room_type, count in available_rooms.items():
            response += f"{room_type.capitalize()} rooms: {count} available\n"
        return response

    def generate_room_number(self, room_type):
        """Generate a random room number based on the room type."""
        prefix = self.room_types[room_type]["prefix"]
        room_number = f"{prefix}{random.randint(1, 99)}"
        return room_number

    def save_booking_to_db(self):
        """Insert the confirmed booking into the MySQL database."""
        room_type = self.context["room_type"]
        fare = self.room_types[room_type]["fare"]
        room_number = self.context["room_number"]

        query = """
            INSERT INTO bookings (name, email, room_type, checkin_date, fare, room_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            self.context["name"],
            self.context["email"],
            room_type,
            self.context["checkin_date"],
            fare,
            room_number
        )
        
        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
            print("Booking saved to DB successfully!")
            self.send_confirmation_email()  
        except mysql.connector.Error as err:
            print("Error saving booking to DB:", err)

    def send_confirmation_email(self):
        """Send a confirmation email to the customer."""
        sender_email = "tanvirrobin0@gmail.com"
        receiver_email = self.context["email"]
        password = "your_email_password_here"
        
        subject = "Hotel Booking Confirmation"
        body = (f"Dear {self.context['name']},\n\n"
                f"Thank you for booking with us! Here are your booking details:\n\n"
                f"Room Type: {self.context['room_type']}\n"
                f"Room Number: {self.context['room_number']}\n"
                f"Check-in Date: {self.context['checkin_date']}\n"
                f"Fare: {self.room_types[self.context['room_type']]['fare']}\n\n"
                "We look forward to your stay with us!\n\nBest regards,\nHotel Team")

        message = MIMEMultipart()
        message["From"] = "Hotel Chatbot"
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print("Confirmation email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

    def get_response(self, user_input):
        """Get bot response based on user input and state."""
        user_input_vector = self.vectorizer.transform([user_input])  
        prediction = self.model.predict(user_input_vector)[0]

        if prediction == "show_available_rooms":
            return self.show_available_rooms()

        if "need a room" in user_input.lower() or "reserve a room" in user_input.lower():
            self.state = "asking_room_type"
        elif "goodbye" in user_input.lower() or "bye" in user_input.lower():
            self.state = None
            self.context = {}

        return prediction

    def chat(self):
        print("Bot: Hello! Welcome to our hotel. How can I assist you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Bot: Thank you for choosing our hotel! Have a great day!")
                break
            response = self.get_response(user_input)
            print("Bot:", response)


if __name__ == "__main__":
    bot = HotelChatBot()
    try:
        bot.chat()
    finally:
        bot.db_cursor.close()
        bot.db_connection.close()
