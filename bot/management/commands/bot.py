import telebot
from telebot import types
from django.core.management.base import BaseCommand

from user.models import User


bot = telebot.TeleBot("You Bot Token")

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        @bot.message_handler(commands=['start'])
        def handle_start(message: types.Message):
            telegram_id = message.from_user.id
            if not User.objects.filter(telegram_id= telegram_id):
                User.objects.create(telegram_id=telegram_id, username=message.from_user.username)
            bot.reply_to(message, f"Welcome to your Django integrated Telegram bot: {message.from_user.username}!")

        @bot.message_handler(commands=['contact'])
        def handle_contact(message):
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            contact_button = types.KeyboardButton(text="Share Contact", request_contact=True)
            keyboard.add(contact_button)
            bot.send_message(message.chat.id, "Please provide your contact information.", reply_markup=keyboard)

        @bot.message_handler(content_types=['contact'])
        def get_contact(message: types.Message):
            phone_number = message.contact.phone_number
            User.objects.filter(telegram_id=message.from_user.id).update(phone_number=phone_number)
            bot.reply_to(message, f"Phone number updated: {phone_number}", reply_markup=types.ReplyKeyboardRemove())


        bot.polling()
