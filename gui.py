import tkinter as tk
from tkinter import messagebox, scrolledtext
from bot import HotelChatBot  

class ChatBotGUI:
    def __init__(self, root):
        self.bot = HotelChatBot()
        self.root = root
        self.root.title("Hotel ChatBot")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        self.font = ("Helvetica", 16)
        self.bot_font = ("Helvetica", 16, "italic")
        self.user_font = ("Helvetica", 16, "bold")

        # Chat log with scrollbar
        self.chat_log_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.chat_log_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.chat_log = scrolledtext.ScrolledText(
            self.chat_log_frame, state="disabled", wrap="word", font=self.font,
            bg="#e6f2ff", fg="#333333", padx=10, pady=10
        )
        self.chat_log.pack(fill="both", expand=True)

        # Input area
        self.input_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.input_frame.pack(pady=10, padx=10, fill="x")

        self.input_field = tk.Entry(self.input_frame, font=self.font, width=60)
        self.input_field.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.input_field.bind("<Return>", self.get_response)

        self.send_button = tk.Button(
            self.input_frame, text="Send", command=self.get_response,
            font=self.font, bg="#007acc", fg="white", relief="raised"
        )
        self.send_button.pack(side="right")

        # Display welcome message
        self.show_welcome_message()

        # Confirm exit on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_welcome_message(self):
        self.display_message("Bot: Hello! Welcome to our hotel. How can I assist you today?", "bot")

    def display_message(self, message, sender):
        """Append messages to the chat log"""
        self.chat_log.config(state="normal")
        tag = "bot" if sender == "bot" else "user"
        
        self.chat_log.insert("end", message + "\n", tag)
        self.chat_log.tag_config("bot", font=self.bot_font, foreground="#0066cc")
        self.chat_log.tag_config("user", font=self.user_font, foreground="#009900")

        self.chat_log.config(state="disabled")
        self.chat_log.yview("end")

    def get_response(self, event=None):
        user_input = self.input_field.get().strip()
        if user_input:
            self.display_message(f"You: {user_input}", "user")
            response = self.bot.get_response(user_input)
            self.display_message(f"Bot: {response}", "bot")
            self.input_field.delete(0, "end")

            if user_input.lower() in ["exit", "quit", "bye"]:
                self.on_closing()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit the chat?"):
            self.bot.db_cursor.close()
            self.bot.db_connection.close()
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()
