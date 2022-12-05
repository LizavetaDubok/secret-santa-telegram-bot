import config
import telebot
from database import DataBase
from random import shuffle

db = DataBase('database.db')
bot = telebot.TeleBot(config.TOKEN)
fixed = False
is_started = False


def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(telebot.types.KeyboardButton(button))
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = generate_buttons(['Стать Сантой'], markup)
    bot.send_message(message.chat.id, 'Привееет, я бот для Тайного Санты Студлиги!')
    bot.send_sticker(message.chat.id,
                     'CAACAgIAAxkBAAEGsV9jjcgcnL0TRHi24pXy7zrOLctBLgACzwADq1fEC6Wy_-K65z0pKwQ')  # хонка
    bot.send_message(message.chat.id, 'Снег уже выпал, гирлянды уже зашуршали, а значит '
                                      'пора задуматься о рождественском турнире, новогодней мафтусовке и, '
                                      'конечно, подарках..\n\n'
                                      '🎄 Ценовой диапазон подарка — 15-20р\n'
                                      '🎄 Окончание регистрации — 6 декабря 23:59\n'
                                      '🎄 Когда сбор? — Выберем дату к Новому году\n'
                                      '🎄 Смогу ли я раздобыть информацию, кто мой Санта? — '
                                      'Нень, бот подконтролен самой неподкупной г-же Лени🦥\n\n'
                                      'Используй меню или команду /join, чтобы вступить в игру', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_(message):
    if message.chat.id in config.admin_chat_id:
        bot.send_message(message.chat.id, '/start\n'
                                          '/join\n'
                                          '/leave\n'
                                          '/wish\n'
                                          '/fix\n'
                                          '/unfix\n'
                                          '/get_participants\n'
                                          '/get_matches\n'
                                          '/match\n'
                                          '/dummy_match\n'
                                          '/play\n'
                                          '/kick\n'
                                          '/notification')
    else:
        bot.send_message(message.chat.id, '/start\n'
                                          '/join\n'
                                          '/leave\n'
                                          '/wish\n')


@bot.message_handler(commands=['join'])
def join(message):
    if db.check_participant(message.chat.id):
        bot.send_message(message.chat.id, 'Ха-ха хитрюшка, два подарка получить не получится. Ты уже играешь')
    elif fixed:
        bot.send_message(message.chat.id, 'А всё, а поздно, а надо было раньше')
        bot.send_sticker(message.chat.id,
                         'CAACAgIAAxkBAAEGsWBjjcgckIH8wWWjWFf9ItfD2A9KywACWhcAAhVy0UomNQvcnMWq1isE')  # лох

    else:
        bot.send_message(message.chat.id, 'Введи ник или имя, если ника пока нет')
        bot.register_next_step_handler(message, after_nick)


def after_nick(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = generate_buttons(['Написать письмо Санте', 'Покинуть игру'], markup)

    db.add_participant(message.chat.id, message.text)

    bot.send_message(message.chat.id, f'Ураа,{db.get_nickname(message.chat.id)}, '
                                      f'ты участница Тайного Санты Студлужи!\n\n'
                                      f'После окончания регистрации я сообщу тебе, кто твоя подопечная, '
                                      f'и поделюсь её вишлистом \n'
                                      f'✨\n'
                                      f'-Бот сделан феминистками..\n'
                                      f'-Сексистками, Тори)\n'
                                      f'✨\n'
                                      f'A пока ты можешь составить список своих пожеланий, '
                                      f'используя меню или команду /wish',
                     reply_markup=markup)

    bot.send_message(message.chat.id, 'Маленькие правила, чтобы все остались довольны: \n'
                                      '🎁 Пиши все свои пожелания одним сообщением в формате списка '
                                      '(если вы напишите два и более сообщения, бот запишет только первое)\n'
                                      '🎁 Пиши конкретно, если указываешь настолки или книги\n'
                                      '🎁 Если вы хотите полностью перезаписать свои пожелания, '
                                      'используйте меню или команду /wish повторно, '
                                      'тогда старое письмо затеряется где-то на почте',
                     reply_markup=markup)
    bot.send_sticker(message.chat.id,
                     'CAACAgUAAxkBAAEGsWFjjcgc1yrMse0CjPjnbWFgmUoLJQACSQcAAszG4gKKHaJFtDWCOSsE')  # lov


@bot.message_handler(commands=['leave'])
def leave(message):
    if not db.check_participant(message.chat.id):
        bot.send_message(message.chat.id, 'Определись....')
    elif fixed:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = generate_buttons(['Написать письмо Санте'], markup)
        bot.send_message(message.chat.id, 'Game has been started, you can\'t escape it muahaha', reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = generate_buttons(['Стать Сантой'], markup)

        db.delete_participant(message.chat.id)
        bot.send_message(message.chat.id, 'Ты куда, Одиссей, от жены, от детей',
                         reply_markup=markup)


@bot.message_handler(commands=['notification'])
def notification(message):
    if message.chat.id in config.admin_chat_id:
        bot.send_message(message.chat.id, 'Введи сообщение')
        bot.register_next_step_handler(message, send_to_all)
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


def send_to_all(message):
    for chat_id in db.get_participants():
        bot.send_message(chat_id, message.text)
    bot.send_message(message.chat.id, 'Done')


def send_wishes_to_santa(chat_id):
    wishes = db.get_participant_wishes(chat_id)
    if wishes:
        bot.send_message(db.get_participant_santa(chat_id),
                         'Хехе, а вот и список пожеланий твоей подопечной:\n' + wishes)
    else:
        bot.send_message(db.get_participant_santa(chat_id),
                         'Бууп, твоя подопечная ещё не написала письмо Санте, '
                         'я пришлю его тебе, когда она его напишет')


@bot.message_handler(commands=['wish'])
def wish(message):
    if db.check_participant(message.chat.id):
        bot.send_message(message.chat.id, 'Напиши письмо своему Санте!')
        bot.register_next_step_handler(message, set_wishes)
    else:
        bot.send_message(message.chat.id, 'Ты не участвуешь в игре и не можешь использовать команду /wish.'
                                          'Сначала вступи в игру')


def set_wishes(message):
    db.set_participant_wishes(message.chat.id, message.text)
    if is_started:
        send_wishes_to_santa(message.chat.id)
    bot.send_message(message.chat.id, 'Письмо отправлено Санте')


@bot.message_handler(commands=['fix'])
def fix(message):
    if message.chat.id in config.admin_chat_id:
        global fixed
        fixed = True
        bot.send_message(message.chat.id, 'Fixed')
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(commands=['kick'])
def kick(message):
    if message.chat.id in config.admin_chat_id:
        bot.register_next_step_handler(message, delete)
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


def delete(message):
    part = db.get_participants()
    if message.text.isdigit() and int(message.text) < len(part):
        db.delete_participant(part[int(message.text)])


@bot.message_handler(commands=['unfix'])
def unfix(message):
    if not is_started:
        bot.send_message(message.chat.id, 'Game is started')
    elif message.chat.id in config.admin_chat_id:
        global fixed
        fixed = False
        bot.send_message(message.chat.id, 'Unfixed')
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(commands=['get_matches'])
def get_matches(message):
    if message.chat.id in config.admin_chat_id:
        matches = db.get_matches()
        str_ = 'Person \t\t\t Santa\n\n'
        for pair in matches:
            str_ += f'{bot.get_chat(pair[0]).first_name} \t\t\t {bot.get_chat(pair[1]).first_name}\n'
        bot.send_message(message.chat.id, str_)
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(commands=['get_participants'])
def get_participants(message):
    if message.chat.id in config.admin_chat_id:
        participants = db.get_participants()
        str_ = f'number of participants: {len(participants)}\n\n'
        i_ = 0
        for chat_id in participants:
            str_ += f'{i_} {bot.get_chat(chat_id).first_name} @{bot.get_chat(chat_id).username}\n'
            i_ += 1
        bot.send_message(message.chat.id, str_)
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(commands=['match'])
def match(message):
    if is_started:
        bot.send_message(message.chat.id, 'Game is started')
    elif message.chat.id in config.admin_chat_id:
        if fixed:
            santas_indices = list(db.get_participants_id())
            shuffle(santas_indices)
            for i in range(len(santas_indices) - 1):
                db.set_santa(santas_indices[i], db.get_chat_id_by_id(santas_indices[i + 1]))
            db.set_santa(santas_indices[-1], db.get_chat_id_by_id(santas_indices[0]))
        else:
            bot.send_message(message.chat.id, 'Fix first')
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(commands=['dummy_match'])
def dummy_match(message):
    if is_started:
        bot.send_message(message.chat.id, 'Game is started')
    elif message.chat.id in config.admin_chat_id:
        if fixed:
            db.make_dummy_matches()
        else:
            bot.send_message(message.chat.id, 'Fix participants first')
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(commands=['play'])
def play(message):
    if message.chat.id in config.admin_chat_id:
        global is_started
        is_started = True
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = generate_buttons(['Покинуть игру', 'Написать письмо Санте'], markup)
        for chat_id in db.get_participants():
            ward_id = db.get_participant_ward(chat_id)
            ward_chat = bot.get_chat(ward_id)
            bot.send_message(chat_id,
                             f'Я объявляю Тайного Санту открытым, '
                             f'похлопайте вашей подопечной - {db.get_nickname(ward_id)}'
                             f'(@{ward_chat.username})',
                             reply_markup=markup)

            bot.send_sticker(chat_id,
                             'CAACAgQAAxkBAAEGsWJjjcgcfF1u1yfIgbPUjlrMbD-yFwACowkAAhsKCFAGbfpeakI6rCsE')  # буп
        for chat_id in db.get_participants():
            send_wishes_to_santa(chat_id)
        bot.send_message(message.chat.id, 'Game has been started')
    else:
        bot.send_message(message.chat.id, 'Sorry, you don\'t have rights to do this')


@bot.message_handler(content_types=['text'], chat_types=['private'])
def bot_message(message):
    if message.text == 'Стать Сантой':
        join(message)

    if message.text == 'Покинуть игру':
        leave(message)

    if message.text == 'Написать письмо Санте':
        wish(message)


bot.polling(none_stop=True)
