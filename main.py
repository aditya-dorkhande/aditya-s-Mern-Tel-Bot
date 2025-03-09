# main.py
import telebot
from telebot import types
from flask import Flask, request
import threading

# ====== YOUR TOKEN ======
TOKEN = "7323834661:AAETevFXymffTUr9UFUi0oYQLG6_Hvd352g"

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Create a Flask web app
app = Flask(__name__)

# --------------------- TELEGRAM BOT HANDLERS ---------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Triggered when the user first opens the bot and taps Telegram's default "Start" button,
    or anytime they type /start in chat.
    """
    # Create a Reply Keyboard with our own single "Start" button
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    custom_start_button = types.KeyboardButton('Start')
    reply_markup.add(custom_start_button)

    bot.send_message(
        message.chat.id,
        "Hello! Tap the 'Start' button below to begin.",
        reply_markup=reply_markup
    )

@bot.message_handler(func=lambda msg: msg.text == "Start")
def handle_custom_start_button(message):
    """
    Triggered when the user taps our custom "Start" button.
    Show them the welcome text and an inline button labeled "Subscribed".
    """
    # Send the Welcome message
    bot.send_message(
        message.chat.id,
        "Welcome to the free MERN-stack web development bot!\n\n"
        "Click the button below to subscribe to my YouTube channel, "
        "then come back and type /subscribe to continue."
    )

    # Create an inline button labeled "Subscribed" linking to your YouTube channel
    subscribe_markup = types.InlineKeyboardMarkup()
    subscribed_button = types.InlineKeyboardButton(
        text="Subscribed",
        url="https://youtube.com/@adityadorkhande01?si=ATlxexGcYhjGLuAL"
    )
    subscribe_markup.add(subscribed_button)

    bot.send_message(
        message.chat.id,
        "Please subscribe and turn on the bell icon for notifications.",
        reply_markup=subscribe_markup
    )

@bot.message_handler(commands=['subscribe'])
def ask_subscription_confirmation(message):
    """
    User types /subscribe after subscribing. We prompt them with two inline buttons:
    "Yes" and "Haa".
    """
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton("Yes", callback_data="subscribed")
    haa_button = types.InlineKeyboardButton("Haa", callback_data="subscribed")
    markup.add(yes_button, haa_button)

    bot.send_message(
        message.chat.id,
        "Have you subscribed to my channel and enabled notifications?",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """
    Handles the user clicking either "Yes" or "Haa" after /subscribe,
    and also handles the 'Next' button callback.
    """
    if call.data == "subscribed":
        # Create inline buttons to Day-1, Day-2, Day-3, plus the Next button
        markup = types.InlineKeyboardMarkup()
        day1_button = types.InlineKeyboardButton(
            "Day-1",
            url="https://drive.google.com/drive/folders/18SzBxtYYYKq1tDHGSnW6AJGoWSZIZoKJ?usp=sharing"
        )
        day2_button = types.InlineKeyboardButton(
            "Day-2",
            url="https://drive.google.com/drive/folders/1LGpS1ME7h4-8zl66VTgvQ3aY3CsqNvfj?usp=sharing"
        )
        next_button = types.InlineKeyboardButton("Next", callback_data="next_step")

        markup.add(day1_button)
        markup.add(day2_button)
        markup.add(next_button)

        bot.send_message(
            call.message.chat.id,
            "Congratulations! Here is your free MERN-stack web development material.\n"
            "This is only the front-end part. The remaining content will be provided "
            "within 10 days after we verify your subscription.\n\n"
            "Enjoy your learning journey!",
            reply_markup=markup
        )

    elif call.data == "next_step":
        # Send the image
        bot.send_photo(
            call.message.chat.id,
            photo="https://s3.ap-south-1.amazonaws.com/rzp-prod-merchant-assets/payment-link/description/pf5jtoqfrcpgfv.jpeg",
            caption="Here's the next step image!"
        )

        # Send a "Go" button that redirects to a link
        go_markup = types.InlineKeyboardMarkup()
        go_button = types.InlineKeyboardButton(
            "Go",
            url="https://superprofile.bio/vp/67cdd291bc7e970013f848a5"
        )
        go_markup.add(go_button)

        bot.send_message(
            call.message.chat.id,
            "Click 'Go' to continue!",
            reply_markup=go_markup
        )

# --------------------- FLASK SETUP FOR REPLIT ---------------------

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_bot():
    """
    Start the Telegram bot's polling in a separate thread so we can
    run Flask below without blocking.
    """
    bot.polling()

# We use threading so that the Flask server and bot.polling() run concurrently
thread = threading.Thread(target=run_bot)
thread.start()

# Run the Flask server on port 8080
app.run(host="0.0.0.0", port=8080)
