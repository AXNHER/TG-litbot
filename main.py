import os
import sqlite3
import time

from telegram import Update, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler, PreCheckoutQueryHandler
from telegram import LabeledPrice, InputMediaPhoto
from telegram import ParseMode

# TOKEN
BOT_TOKEN = ''

# Conversation states
USER_INFO, QUESTION = range(2)

kos = 0
til = 0

# Database initialization
conn = sqlite3.connect('user_info.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                  (user_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT,
                   paid INTEGER DEFAULT 0, current_question_counter INTEGER DEFAULT 0,
                   answered_questions INTEGER DEFAULT 0)''')
conn.commit()

# QUESTIONS
personal_info_questions = [
    {
        "text": "Привет! Это чат-бот «Прогульщики» школы текстов «Мне есть что сказать». Прямо сейчас мы вместе отправимся на писательскую прогулку. Будем гулять, наблюдать, останавливаться и писать небольшие художественные зарисовки. Наши писательские упражнения помогут вам поймать творческую волну. \n\nНо сначала — пара коротких вопросов! Как можно к вам обращаться? Напишите имя.\n",
        "next_question": "last_name",
    },
    {
        "text": "А теперь фамилию.",
        "next_question": "email",
    },
    {
        "text": "Приятно познакомиться! Чтобы мы не потеряли с вами связь, укажите свой имейл.",
        "next_question": "done",
    },
]

questions = [
    {
        "text": "Question 0: PAY",
        "info_button": "info0",
        "info_text": "Additional info for Question 0.",
        "next_button": "Next0",
    },
    {
        #1
        "text": "Отлично, мы готовы отправиться в путь! Одного правильного маршрута у прогулки нет — мы предлагаем построить его самим с нашими подсказками. Выходите на улицу, где бы вы ни оказались: во дворе вашего детства или в незнакомом городе. Считайте это первым заданием.",
        #"info_button": "info1",
        #"info_text": "Additional info for Question 1.",
        "next_button": "Как работает бот?",
        "photos": ["image0.jpg", "image01.jpg"],
        "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        #"response": "Reading"
    },
    {
        # 2
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 1
        "text": "И тд",
        # "info_button": "info1",
        # "info_text": "Additional info for Question 1.",
        "next_button": "Далее",
        # "photos": ["image0.jpg", "image01.jpg"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3"
        # "response": "Reading"
    },
    {
        # 23
        "text": "Пройти бота еще раз?",
        # "info_button": "Пример для вдохновения",
        # "info_text": "На письме возможно все, поэтому повествование, в центре которого находится неживой объект — не такой уж и странный прием. У Виктора Пелевина есть рассказ  «Жизнь и приключения сарая Номер XII», где главный герой — сарай, мечтающий стать велосипедом.",
        "next_button": "/start",
        # "photos": ["image4.png"],
        # "audio": "The_Durutti_Column_-_Sketch_for_Summer.mp3",
        # "response": "Это было непростое задание, но вы справились. Похвалите себя, этот монолог города может стать потом частью вашего рассказа!"
    },
]

def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_data = context.user_data

    user_data['chat_id'] = chat_id

    # Create a new SQLite connection and cursor
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    # Check if the user's information already exists in the database
    cursor.execute("SELECT * FROM user_info WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        user_data['current_question_idx'] = existing_user[5]  # Restore current question counter
    else:
        user_data['current_question_idx'] = 0  # Initialize current_question_idx

    conn.close()

    if user_data['current_question_idx'] == 0:
        return ask_user_info(update, context)  # Start collecting personal information
    else:
        return ask_question(update, context)  # Proceed to the main questions

def ask_payment(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id

    # Create a new SQLite connection and cursor
    new_conn = sqlite3.connect('user_info.db')
    new_cursor = new_conn.cursor()

    # Check if the user has answered the second question
    new_cursor.execute("SELECT paid FROM user_info WHERE user_id=?", (user_id,))
    user_info = new_cursor.fetchone()
    print("PAYDAY")
    if user_info[0] == 0:
        new_conn.close()  # Close the connection
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Оплатите бота, чтобы продолжить",
        )
        context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title="Payment",
            description="wordstowalk_bot",
            payload="QUESTION_PAYMENT",
            provider_token='',  # Replace with your actual provider token
            currency='RUB',  # Specify the correct currency code for Russian rubles
            prices=[LabeledPrice(label='Question Payment', amount=990 * 100)],  # 990 rubles
            start_parameter='payment-question',
        )
        return ConversationHandler.END  # End the conversation here/
    else:
        new_conn.close()  # Close the connection
        return next_question(update, context)  # Proceed to the first question

def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    print(query)
    if query.invoice_payload == 'QUESTION_PAYMENT':
        user_id = query.from_user.id

        context.bot.answer_pre_checkout_query(
            pre_checkout_query_id=query.id,
            ok=True
        )
        context.bot.send_message(
            chat_id=query.from_user.id,
            text="Платеж принят в обработку. Пожалуйста, завершите покупку."
        )

        # Retrieve the stored update and context objects
        stored_update = context.user_data.get('update')
        stored_context = context.user_data.get('context')

        return start  # Proceed to the next question

    # Close the new connection
        new_conn.close()

def successful_payment(update, context):
    print("SUCCESSFUL PAYMENT:")

    total_amount = update.message.successful_payment.total_amount // 100
    currency = update.message.successful_payment.currency
    invoice_payload = update.message.successful_payment.invoice_payload

    print(f"Total Amount: {total_amount} {currency}")
    print(f"Invoice Payload: {invoice_payload}")

    # Update answered questions count for the user
    user_id = update.effective_user.id
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET paid = 1 WHERE user_id = ?", (user_id,))
    cursor.execute("UPDATE user_info SET current_question_counter = current_question_counter + 1 WHERE user_id = ?",
                   (user_id,))
    conn.commit()
    conn.close()

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Платеж в размере {total_amount} {currency} был обработан! Если следующий вопрос не появится автоматически пропишите /start в чат."
    )

def ask_user_info(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'css_counter' not in user_data:
        user_data['css_counter'] = 0

    print(user_data['css_counter'])

    i = 0

    question_idx = user_data['css_counter']
    question = personal_info_questions[question_idx]

    if question["next_question"] == "first_name":
        user_data['first_name'] = update.message.text
    elif question["next_question"] == "last_name" :
        user_data['last_name'] = update.message.text
    elif question["next_question"] == "email":
        user_data['email'] = update.message.text

        user_id = update.message.from_user.id
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        email = user_data['email']

        # Create a new SQLite connection and cursor
        new_conn = sqlite3.connect('user_info.db')
        new_cursor = new_conn.cursor()

        # Check if the user's information already exists in the database
        new_cursor.execute("SELECT * FROM user_info WHERE user_id=?", (user_id,))
        existing_user = new_cursor.fetchone()

        if existing_user:
            update.message.reply_text("Your information already exists in the database. "
                                      "Thank you for providing it again.")
        else:
            new_cursor.execute("INSERT INTO user_info (user_id, first_name, last_name, email, answered_questions) "
                               "VALUES (?, ?, ?, ?, 0)",
                               (user_id, first_name, last_name, email))
            new_conn.commit()
            # update.message.reply_text("Thank you for providing your information. It has been recorded in the database.")

        # Close the new connection
        new_conn.close()

        user_data['css_counter'] = 0


    question_idx = user_data.get('css_counter', 0)
    question = personal_info_questions[question_idx]
    update.message.reply_text(question["text"])
    user_data['css_counter'] += 1
    return USER_INFO

def next_personal_info_question(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['current_question_idx'] += 1
    question_idx = user_data['current_question_idx']
    question = personal_info_questions[question_idx]
    update.message.reply_text(question["text"])
    return USER_INFO

def receive_user_info(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    question_idx = user_data.get('current_question_idx', 0)
    question = personal_info_questions[question_idx]

    if question["next_question"] == "last_name":
        user_data['first_name'] = update.message.text
    elif question["next_question"] == "email":
        user_data['last_name'] = update.message.text
    elif question["next_question"] == "done":
        user_data['email'] = update.message.text

        user_id = update.message.from_user.id
        first_name = user_data['first_name']
        last_name = user_data.get('last_name', '')
        email = user_data['email']

        # Create a new SQLite connection and cursor
        new_conn = sqlite3.connect('user_info.db')
        new_cursor = new_conn.cursor()

        # Check if the user's information already exists in the database
        new_cursor.execute("SELECT * FROM user_info WHERE user_id=?", (user_id,))
        existing_user = new_cursor.fetchone()

        if existing_user:
            update.message.reply_text("Your information already exists in the database. "
                                      "Thank you for providing it again.")
        else:
            new_cursor.execute("INSERT INTO user_info (user_id, first_name, last_name, email, answered_questions) "
                               "VALUES (?, ?, ?, ?, 0)",
                               (user_id, first_name, last_name, email))
            new_conn.commit()
            #update.message.reply_text("Thank you for providing your information. It has been recorded in the database.")

        # Close the new connection
        new_conn.close()

        user_data['current_question_idx'] = 0  # Reset the counter
        return next_question(update, context)  # Proceed to next question

    user_data['current_question_idx'] += 1
    question_idx = user_data.get('current_question_idx', 0)
    question = personal_info_questions[question_idx]
    update.message.reply_text(question["text"])
    return USER_INFO

def ask_question(update: Update, context: CallbackContext) -> int:
    print(update, context)
    user_data = context.user_data
    question_idx = user_data['current_question_idx']
    question = questions[question_idx]
    media_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Media')
    user_id = update.effective_user.id

    # Create a new SQLite connection and cursor
    new_conn = sqlite3.connect('user_info.db')
    new_cursor = new_conn.cursor()

    # Check if the user has answered the second question
    new_cursor.execute("SELECT paid FROM user_info WHERE user_id=?", (user_id,))
    user_info = new_cursor.fetchone()
    print(question_idx ,user_info[0])

    if question_idx >= 7 and user_info[0] == 0:
        user_data['update'] = update
        user_data['context'] = context
        return ask_payment(update, context)

    # Send the reply keyboard markup without the text message
    if "info_button" in question:
        keyboard = [
            [KeyboardButton(text=question["info_button"]), KeyboardButton(text=question["next_button"])]
        ]
    else:
        keyboard = [
            [KeyboardButton(text=question["next_button"])]
        ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if question_idx == 19:
        context.bot.send_message(chat_id=update.effective_chat.id, text=question.get("text", ""), reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=question.get("text", ""),
                                 parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup, disable_web_page_preview=True)

    if "photos" in question:
        photo_media = []
        for photo_filename in question["photos"]:
            photo_path = os.path.join(media_folder, photo_filename)
            photo_media.append(InputMediaPhoto(media=open(photo_path, 'rb')))
        context.bot.send_media_group(update.effective_chat.id, photo_media)

    if "audio" in question:
        audio_path = os.path.join(media_folder, question["audio"])
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_path, 'rb'))


    # Use update.effective_user.id to get the user ID
    user_id = update.effective_user.id

    # Update the current question counter in the database
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    if user_data['current_question_idx'] == 23:
        cursor.execute("UPDATE user_info SET current_question_counter = ? WHERE user_id = ?",
                       (1, user_id))
        conn.commit()
        conn.close()
        return ConversationHandler.END

    else:
        cursor.execute("UPDATE user_info SET current_question_counter = ? WHERE user_id = ?", (user_data['current_question_idx'], user_id))
        conn.commit()
        conn.close()

    return QUESTION

def receive_answer(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    response = update.message.text
    question = questions[user_data['current_question_idx']]

    if "info_button" in question and response == question["info_button"]:
        update.message.reply_text(question["info_text"], parse_mode=ParseMode.MARKDOWN)
        return QUESTION

    response_text = question.get("response", "")  # Use default empty string if "response" key is not present

    if response == question["next_button"] and user_data['current_question_idx'] < len(questions) - 1:
        user_id = update.message.from_user.id

        # Update answered questions count for the user
        conn = sqlite3.connect('user_info.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_info SET answered_questions = answered_questions + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

        user_data['current_question_idx'] += 1

        return ask_question(update, context)
    else:
        update.message.reply_text(response_text)  # Send the correct response text
        return QUESTION

def next_question(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['current_question_idx'] += 1

    user_id = update.effective_user.id
    new_conn = sqlite3.connect('user_info.db')
    new_cursor = new_conn.cursor()
    new_cursor.execute("UPDATE user_info SET current_question_counter = ? WHERE user_id = ?", (user_data['current_question_idx'], user_id))
    new_conn.commit()
    new_conn.close()

    print(user_data['current_question_idx'])
    if user_data['current_question_idx'] < 22:
        return ask_question(update, context)
    else:
        response_text = "Напишите /start в чат, чтобы начать прогулку заново"
        update.message.reply_text(response_text)

        user_id = update.effective_user.id
        new_conn = sqlite3.connect('user_info.db')
        new_cursor = new_conn.cursor()
        new_cursor.execute("UPDATE user_info SET current_question_counter = 1 WHERE user_id = ?",
                           (user_id))
        new_conn.commit()
        new_conn.close()
        user_data.clear()
        return ConversationHandler.END

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USER_INFO: [MessageHandler(Filters.text & ~Filters.command, receive_user_info)],
            QUESTION: [MessageHandler(Filters.text & ~Filters.command, receive_answer)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    successful_payment_handler = MessageHandler(Filters.successful_payment, successful_payment)
    dispatcher.add_handler(successful_payment_handler)

    updater.start_polling(poll_interval=1)
    updater.idle()

if __name__ == '__main__':
    main()