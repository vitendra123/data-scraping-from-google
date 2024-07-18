import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from twilio.rest import Client
from googletrans import Translator
import json
import getpass

# Sample data for bot training
call_data = [
    {"input": "Hello, can I speak to the business owner?", "response": "Sure, how can I help you?"},
    {"input": "We offer business loans. Are you interested?", "response": "Yes, tell me more about it."},
    {"input": "Can we book an appointment to discuss further?", "response": "Sure, when are you available?"},
]

# Preprocess data
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts([pair["input"] for pair in call_data])
input_sequences = tokenizer.texts_to_sequences([pair["input"] for pair in call_data])
input_padded = pad_sequences(input_sequences, padding='post')

# Model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=10000, output_dim=64, input_length=input_padded.shape[1]),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(tokenizer.word_index) + 1, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Dummy target data (for demonstration purposes)
target_sequences = tokenizer.texts_to_sequences([pair["response"] for pair in call_data])
target_padded = pad_sequences(target_sequences, padding='post')

# Train the model
model.fit(input_padded, target_padded, epochs=10)

# Save the model
model.save("cold_calling_bot.h5")

# Load the trained model
model = tf.keras.models.load_model("cold_calling_bot.h5")

# Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

# Translator setup
translator = Translator()

# User database (for simplicity, using a JSON file)
user_db = "users.json"

def load_users():
    try:
        with open(user_db, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(user_db, "w") as file:
        json.dump(users, file)

def register():
    users = load_users()
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        return
    password = getpass.getpass("Enter password: ")
    users[username] = password
    save_users(users)
    print("Registration successful.")

def login():
    users = load_users()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if users.get(username) == password:
        print("Login successful.")
        return True
    else:
        print("Invalid username or password.")
        return False

def make_call(message, to):
    call = client.calls.create(
        twiml=f'<Response><Say>{message}</Say></Response>',
        to=to,
        from_='your_twilio_phone_number'
    )
    print("Call initiated:", call.sid)

def generate_response(input_text):
    input_seq = tokenizer.texts_to_sequences([input_text])
    input_padded = pad_sequences(input_seq, maxlen=input_padded.shape[1], padding='post')
    prediction = model.predict(input_padded)
    response_seq = prediction.argmax(axis=-1)
    response_text = tokenizer.sequences_to_texts(response_seq)
    return response_text[0]

def main():
    print("Welcome to the Cold Calling Bot")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            register()
        elif choice == "2":
            if login():
                while True:
                    message = input("Enter the message to send (or 'exit' to log out): ")
                    if message == 'exit':
                        break
                    language = input("Enter language code (e.g., 'en' for English, 'es' for Spanish): ")
                    translated_message = translator.translate(message, dest=language).text
                    to = input("Enter the recipient's phone number: ")
                    make_call(translated_message, to)
            else:
                print("Login failed. Try again.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
