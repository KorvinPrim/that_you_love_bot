from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def data(bot, update):
    update.message.reply_text(time.asctime())


def echo(bot, update):
    mess = update.message.text
    update.message.reply_text(mess[::-1])


def start(bot, update):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад! Попробуй ввести своё имя и посмотри что будет!",
        reply_markup=markup)

def close(bot, update):
    update.message.reply_text("Ok", reply_markup=ReplyKeyboardRemove())

def unset_timer(bot, update, chat_data):
    # Проверяем, что задача ставилась. (вот зачем нужно было ее записать в chat_data)
    if 'job' in chat_data:
        # планируем удаление задачи (выполнется, когда будет возможность)
        chat_data['job'].schedule_removal()
        # и очищаем пользовательские данные
        del chat_data['job']

    update.message.reply_text('Хорошо, вернулся сейчас!')

def task(bot, job):
    bot.send_message(job.context, text='Вернулся!')

def set_timer(bot, update, job_queue, chat_data, args):
    # создаем задачу task в очереди job_queue через 20 секунд
    # передаем ей идентификатор текущего чата (будет доступен через job.context)
    update.message.reply_text(args)
    job = job_queue.run_once(task, int(args[0]), context=update.message.chat_id)

    # Запоминаем в пользовательских данных созданную задачу.
    chat_data['job'] = job

    # Присылаем сообщение о том, что все получилось.
    update.message.reply_text('Вернусь через '+args[0]+' секунд!')


def main():
    updater = Updater("568556775:AAHsW06Q7g6qd-K7FQS3d5XBk4xGTqxArc8")
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(CommandHandler("data", data))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("set_timer", set_timer, pass_job_queue=True, pass_chat_data=True, pass_args=True))
    dp.add_handler(CommandHandler("unset_timer", unset_timer, pass_chat_data=True))
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()