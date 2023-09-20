import logging
import telebot
import constants
from datetime import datetime
import b_data

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

def femrulit_birthBot(token: str) -> None:
    bot = telebot.TeleBot(token, parse_mode=None)

    # обрабатываем команды
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, 'Привет! Я показываю, у кого из русских писательниц когда день рождения. Введи дату в формате ДД.ММ или напиши "сегодня".')

    # главная функция
    def main(message, date_str):
        def check_birthdays(target_date):
            birthdays = []

            for day, data in b_data.september.items():
                if day == target_date:
                    if isinstance(data, str):
                        birthdays.append(data)
                    else:
                        birthdays.extend(data)

            return birthdays

        birthdays = check_birthdays(date_str)

        if birthdays:
            if len(birthdays) == 1:
                response_text = f'{birthdays[0]} родилась в этот день'
            else:
                response_text = '\n'.join([f'{name}' for name in birthdays]) + ' родились в этот день'

            bot.send_message(message.chat.id, response_text)
        else:
            bot.send_message(message.chat.id, 'Не могу найти никого из русских писательниц, кто родилась бы в этот день.')

    # обрабатываем входящие сообщения
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        date_str = message.text.strip()
        if date_str.lower() == 'сегодня':
            today = datetime.now().strftime('%d.%m')
            main(message, today)
        else:
            # Разбор даты с учетом нового формата
            try:
                parsed_date = datetime.strptime(date_str, '%d.%m')
                date_str = parsed_date.strftime('%d.%m')
                main(message, date_str)
            except ValueError:
                bot.send_message(message.chat.id, 'Введи дату в формате ДД.ММ или напиши "сегодня".')

    # запустить бота
    bot.polling()

if __name__ == '__main__':
    femrulit_birthBot(constants.TOUR_TELEGRAM_TOKEN)