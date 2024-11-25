import random
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


training_data = [
    ("What is your menu?", "Here is our menu:\nPizza: BDT 100\nBurger: BDT 50\nPasta: BDT 70\nSalad: BDT 40\nSoda: BDT 20"),
    ("Show me the menu", "Here is our menu:\nPizza: BDT 100\nBurger: BDT 50\nPasta: BDT 70\nSalad: BDT 40\nSoda: BDT 20"),
    ("I want to order something", "Sure! Please tell me what you'd like to order."),
    ("Can I order food?", "Sure! Please tell me what you'd like to order."),
    ("I would like to order a pizza", "Added Pizza to your order. Would you like to add something else?"),
    ("Can I have a burger?", "Added Burger to your order. Would you like to add something else?"),
    ("I would like some pasta", "Added Pasta to your order. Would you like to add something else?"),
    ("Can I get a salad?", "Added Salad to your order. Would you like to add something else?"),
    ("I'd like a soda", "Added Soda to your order. Would you like to add something else?"),
    ("No, that's all", "Thank you! Could you provide your delivery address?"),
    ("Please give me your name", "Thank you! Could you provide your name?"),
    ("My name is John", "Thank you, John! Could you provide your delivery address?"),
    ("My address is 123 Main Street", "Thank you for your order, John! It will be delivered to 123 Main Street. Your total is BDT 150."),
    ("Goodbye", "Goodbye! Have a great day!"),
    ("Bye", "Goodbye! Have a great day!"),
    ("Thank you", "You're welcome! Have a great day!"),
    ("Can I change my order?", "Sure! What would you like to change in your order?"),
    ("I want to cancel my order", "Sorry to hear that. Your order has been canceled."),
    ("What are your hours?", "We are open from 10 AM to 10 PM every day."),
    ("Do you offer delivery?", "Yes, we offer delivery within a 5-mile radius."),
    ("How long does delivery take?", "Delivery usually takes between 30 to 45 minutes."),
    ("Can I make a reservation?", "Yes, you can make a reservation by providing your name, date, and time."),
    ("Do you have vegan options?", "Yes, we have vegan options available. Please check our menu."),
    ("What payment methods do you accept?", "We accept cash, credit cards, and mobile payments."),
    ("Can I pay online?", "Yes, you can pay online through our website."),
    ("Do you have gluten-free options?", "Yes, we offer gluten-free options. Please check our menu."),
    ("Can I get a discount?", "We offer discounts on special occasions. Please check our website for current offers."),
    ("Do you have a kids' menu?", "Yes, we have a kids' menu with smaller portions and lower prices."),
    ("What is your address?", "Our restaurant is located at 456 Elm Street."),
    ("Can I cancel my reservation?", "Yes, you can cancel your reservation by providing your name and reservation details."),
    ("Do you have outdoor seating?", "Yes, we have outdoor seating available."),
    ("Is there parking available?", "Yes, we have a parking lot available for our customers."),
    ("Do you offer catering services?", "Yes, we offer catering services for events and parties."),
    ("Can I see the dessert menu?", "Here is our dessert menu:\nIce Cream: BDT 30\nCake: BDT 40\nPie: BDT 50"),
    ("Do you have any specials today?", "Yes, we have a special on our pasta dishes today. Please check our menu for details.")
]

class RestaurantChatBot:
    def __init__(self):
        self.context = {}
        self.training_data = self.create_training_data()
        self.vectorizer, self.model = self.train_model()
        self.state = None

        
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="restaurant_chatbot"
        )
        self.db_cursor = self.db_connection.cursor()

    def create_training_data(self):
        return training_data

    def train_model(self):
        X = [text for text, response in self.training_data]
        y = [response for text, response in self.training_data]

        vectorizer = TfidfVectorizer()
        model = LogisticRegression()
        pipeline = make_pipeline(vectorizer, model)
        pipeline.fit(X, y)

        return vectorizer, model

    def save_order_to_db(self):
        """Insert the confirmed order into the MySQL database."""
        food_items = ', '.join(self.context["order_items"])
        total_price = sum(self.context["order_prices"])

        query = """
            INSERT INTO orders (name, address, order_items, total_price)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            self.context["name"],
            self.context["address"],
            food_items,
            total_price
        )
        
        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
            print("Order saved to DB successfully!")
        except mysql.connector.Error as err:
            print("Error saving order to DB:", err)

    def get_response(self, user_input):
        
        if self.state == "asking_name":
            if user_input.strip():
                self.context["name"] = user_input
                self.state = "asking_address"
                return "Thank you, {0}. Could you please provide your delivery address?".format(self.context["name"])
            else:
                return "Please provide your name."

        if self.state == "asking_address":
            self.context["address"] = user_input
            self.state = "order_complete"
            self.save_order_to_db()
            # return f"Thank you for your order, {self.context['name']}! Your total is ${sum(self.context['order_prices'])}. It will be delivered to {self.context['address']}."
            self.context["order_id"] = random.randint(1000, 9999)
            return f"Thank you for your order, {self.context['name']}! Your order ID is #{self.context['order_id']}. Your total is ${sum(self.context['order_prices'])}. It will be delivered to {self.context['address']}."

        
        user_input_vector = self.vectorizer.transform([user_input])  
        prediction = self.model.predict(user_input_vector)[0]

        
        if any(item in user_input.lower() for item in ["pizza", "burger", "pasta", "salad", "soda"]):
            food_item = None
            price = 0
            if "pizza" in user_input.lower():
                food_item, price = "Pizza", 10
            elif "burger" in user_input.lower():
                food_item, price = "Burger", 5
            elif "pasta" in user_input.lower():
                food_item, price = "Pasta", 7
            elif "salad" in user_input.lower():
                food_item, price = "Salad", 4
            elif "soda" in user_input.lower():
                food_item, price = "Soda", 2

            if "order" not in self.context:
                self.context["order_items"] = []
                self.context["order_prices"] = []

            self.context["order_items"].append(food_item)
            self.context["order_prices"].append(price)

            return f"Added {food_item} to your order. Would you like to add something else?"

        
        if "no" in user_input.lower() or "that's all" in user_input.lower():
            self.state = "asking_name"
            return "Great! Could you please provide your name?"

        
        if "goodbye" in user_input.lower() or "bye" in user_input.lower():
            self.state = None
            self.context = {}
            return "Goodbye! Have a great day!"

        return prediction

    def chat(self):
        print("Bot: Welcome to our restaurant! How can I assist you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Bot: Thank you for choosing our restaurant! Have a great day!")
                break
            response = self.get_response(user_input)
            print("Bot:", response)


if __name__ == "__main__":
    bot = RestaurantChatBot()
    try:
        bot.chat()
    finally:
        bot.db_cursor.close()
        bot.db_connection.close()
