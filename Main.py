from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import sys
import requests
import time
import wikipedia
wikipedia.set_lang('ru')

class Get_link:
    def geocoder_request(self, **kwargs):
        try:
            post = []
            for key, val in kwargs.items():
                post.append(key + '=' + val)
            print(post)
            address = 'http://geocode-maps.yandex.ru/1.x/?' + '&'.join(post)

            response = requests.get(address)

            if not response:
                print('Ошибка выполнения запроса:')
                print('Http статус: {} ({})'.format(response.status_code, response.reason))
                sys.exit(1)

            return json.loads(response.text)

        except:
            print('Запрос не удалось выполнить. Проверьте наличие сети Интернет.')
            sys.exit(1)

    def link(self, **kwargs):
        try:
            post = []
            for key, val in kwargs.items():
                post.append(str(key) + '=' + str(val))

            map_request = "http://static-maps.yandex.ru/1.x/?{}".format('&'.join(post))

            return map_request

        except:
            print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
            sys.exit(1)

    def geocode(self,address):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={address}&format=json".format(**locals())
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
        else:
            raise RuntimeError(
                """Ошибка выполнения запроса:
                {request}
                Http статус: {status} ({reason})""".format(
                    request=geocoder_request, status=response.status_code, reason=response.reason))
        features = json_response["response"]["GeoObjectCollection"]["featureMember"]

        return features[0]["GeoObject"] if features else None

    def get_coordinates(self,address):
        toponym = self.geocode(address)
        if not toponym:
            return False
        toponym_coodrinates = toponym["Point"]["pos"]

        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        return [float(toponym_longitude), float(toponym_lattitude)]

    def return_link(self,inquiry):
        coord = self.get_coordinates(inquiry)
        try:
            return self.link(ll='{0},{1}'.format(str(coord[0]), str(coord[1])),
                                                    z=5, l='sat,skl')
        except Exception:
            return self.link(ll='{0},{1}'.format(str(0.0), str(0.0)),
                             z=0, l='sat,skl')


def return_data_to_lend(bot, update, chat_data):
    continuation = [['Получить помощь по путешествию'], ['Особенности страны']]
    continuation_markup = ReplyKeyboardMarkup(continuation, one_time_keyboard=True)

    countries = [[[[['Катар', 'Вьетнам'], ['Объединённые Арабские Эмираты', 'Бахрейн'], ['Мексика', 'Ямайка']],
                   [['Малазия', 'Турция'], ['Тайланд', 'Сейшелы'], ['Мексика', 'Албания']],
                   [['Багамы', 'Зимбабве'], ['Катар', 'Кения'], ['Куба', 'Мальдивы']],
                   [['Мальта', 'Мексика'], ['Сейшелы', 'Тунис'], ['Боствана', 'Объединённые Арабские Эмираты']]],
                  [[['Ямайка', 'Индия'], ['Бахрейн', 'Катар'], ['Аруба', 'Непал']],
                   [['Гаити', 'Южный Судан'], ['Нигерия', 'Демократическая Республика Конго'],
                    ['Камерун', 'Кения']],
                   [['Гаити', 'Марокко'], ['Куба', 'Мальдивы'], ['Сейшелы', 'Объединённые Арабские Эмираты']],
                   [['Австрия', 'Андорра'], ['Бразилия', 'Перу'], ['Тунис', 'Исландия']]]], [
                     [[['Англия', 'Ирландия'], ['Люксембург', 'Германия'], ['Италия', 'Финляндия']],
                      [['Австралия', 'Австрия'], ['Бельгия', 'Великобритания'], ['Германия', 'Ирландия']],
                      [['Лихтенштейн', 'Люксембург'], ['Нидерланды', 'Франция'], ['Швейцария', 'Белоруссия']],
                      [['Болгария', 'Венгрия'], ['Молдавия', 'Польша'], ['Россия', 'Румыния']]],
                     [[['Словакия', 'Чехия'], ['Украина', 'Дания'], ['Исландия', 'Латвия']],
                      [['Литва', 'Норвегия'], ['Финляндия', 'Эстония'], ['Швеция', 'Албания']],
                      [['Андорра', 'Босния и Герцеговина'], ['Ватикан', 'Греция'], ['Испания', 'Италия']],
                      [['Македония', 'Мальта'], ['Португалия', 'Сан-Марино'], ['Новая Зеландия', 'Руанда ']]]]]

    lend = str(countries[chat_data['climate']][chat_data['type_of_rest']]
               [chat_data['money']][chat_data['visa']][
                   chat_data['children']])

    update.message.reply_text('Мы рекомендуем вам посетить страну: ' + lend, reply_markup=continuation_markup)
    try:
        bot.send_photo(update.message.chat_id, Get_link().return_link(lend))
    except Exception:
        update.message.reply_text('Картинка недоступна.')
    update.message.reply_text('По данным cайта wikipedia.org: ' + wikipedia.summary(lend))


def data(bot, update):
    update.message.reply_text(time.asctime())


def echo(bot, update, chat_data):
    if len(chat_data) != 0:
        pass


def calibration(bot, update, chat_data):
    print(update.message.text)
    if update.message.text != '/start':
        climat = [['Жаркий', 'Умеренный']]
        type_of_rest = [['Экей тюленик на пляжу', 'Исследователь'], ['Культурный гуру', 'Венера fm']]
        money = [['Дайте хлеба', 'Ммм... маслоу'], ['Неплохой айфон', 'Налог?.. пффф.']]
        visa = [['Я не умею писать.', 'Знаю алфавит.', 'Стоять насмерть!']]
        children = [['Дети? Бее...', 'Ути какие щёчки!']]

        if ('climate' not in chat_data) and (update.message.text in climat[0]):
            chat_data['climate'] = climat[0].index(update.message.text)
        if ('type_of_rest' not in chat_data) and (
                        update.message.text in type_of_rest[0] or update.message.text in type_of_rest[1]):
            chat_data['type_of_rest'] = (type_of_rest[0].index(update.message.text) if update.message.text in
                                                                                       type_of_rest[0] else
                                         type_of_rest[1].index(update.message.text)) % 2
        if ('money' not in chat_data) and (update.message.text in money[0] or update.message.text in money[1]):
            chat_data['money'] = money[0].index(update.message.text) if update.message.text in money[0] else money[
                1].index(update.message.text)
        if ('visa' not in chat_data) and (update.message.text in visa[0]):
            chat_data['visa'] = visa[0].index(update.message.text)
        if ('children' not in chat_data) and (update.message.text in children[0]):
            chat_data['children'] = children[0].index(update.message.text)

        if 'climate' not in chat_data:
            markup = ReplyKeyboardMarkup(climat, one_time_keyboard=True)
            update.message.reply_text('Какой климат вам больше нравиться?', reply_markup=markup)

        elif 'type_of_rest' not in chat_data:
            type_of_rest_mak = ReplyKeyboardMarkup(type_of_rest, one_time_keyboard=True)
            update.message.reply_text('Какой вид отдыха вам больше симпотизирует?', reply_markup=type_of_rest_mak)

        elif 'money' not in chat_data:
            moneyt_mak = ReplyKeyboardMarkup(money, one_time_keyboard=True)
            update.message.reply_text('Какая фраза лучше описывает ваше финансовое положение?', reply_markup=moneyt_mak)

        elif 'visa' not in chat_data:
            visa_mak = ReplyKeyboardMarkup(visa, one_time_keyboard=True)
            update.message.reply_text('Охарактеризуйте ваше желание тоскаться за бумагами для визы.',
                                      reply_markup=visa_mak)

        elif 'children' not in chat_data:
            children_mak = ReplyKeyboardMarkup(children, one_time_keyboard=True)
            update.message.reply_text('Будите ли вы брать в путешествие детей?', reply_markup=children_mak)

    if 'children' in chat_data:
        return_data_to_lend(bot, update, chat_data)

    print(chat_data)


def start(bot, update, job_queue, chat_data):
    reply_keyboard = [['Получить страну!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Привет! Я бот-помошник путешествий, я помогу тебе выбрать место куда можно поехать отдохнуть! Чтобы узнать твои предпочтения я задам тебе несколько вопросов, просто нажимай на вариант который тебе больше по душе. Для начала нажми:",
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


def main():
    updater = Updater("568556775:AAHsW06Q7g6qd-K7FQS3d5XBk4xGTqxArc8")
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, calibration, pass_chat_data=True)

    dp.add_handler(CommandHandler("data", data))
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("close", close))

    # dp.add_handler(CommandHandler("set_timer", set_timer, pass_job_queue=True, pass_chat_data=True, pass_args=True))
    # dp.add_handler(CommandHandler("unset_timer", unset_timer, pass_chat_data=True))

    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
