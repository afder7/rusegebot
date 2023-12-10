import telebot
import random
import datetime
import asyncio


with open("slovnik.txt", "r", encoding="utf-8") as f:
    s = list(filter(lambda x: x, f.read().split("\n")))

bit = telebot.TeleBot("6874264125:AAGu5zoLMosurFlDses77TthwCmcZ1tTVhw")

# user: time to send new message every day
users = dict()

loop = asyncio.get_event_loop()


def pick_words():
    #выбираем 6 слов из словника, которые отправим человечку
    random.shuffle(s)
    words = "\n".join(s[:6])
    return words


@bit.message_handler(content_types=['text'])
def start(msg):
    if msg.text == "/start":
        bit.send_message(msg.from_user.id, "Привет, я бот, который поможет тебе выучить ударения для ЕГЭ по русскому языку!\n"
                                           "Каждый день я буду отправлять тебе 6 слов, ты будешь читать их, они отложатся в памяти и в конце концов ты выучишь слова, тратя на это по полминуты в день!\n"
                                           "Чтобы начать пользоваться введи время, в которое я должен отправлять тебе новые слова каждый день, в формате часы:минуты (например 10:00 или 22:10). Моё время  - GMT +3\n"
                                           "Мой создатель @redfa7 или @afder7 подписывайся, если что :)")
        bit.register_next_step_handler(msg, add_user)
    else:
        bit.send_message(msg.from_user.id, "Отправь /start чтобы начать")


def add_user(msg):
    print(msg)
    t = msg.text
    try:
        te = t.split(":")
        print(te)
        if -1 < int(te[0]) < 24 and -1 < int(te[1]) < 60:
            global users
            users[msg.from_user.id] = ((int(te[0]) - 3) % 24) * 60 * 60 + int(te[1]) * 60
            bit.send_message(msg.from_user.id, "Отлично, уже завтра или сегодня (в зависимости от времени, когда ты мне пишешь) я отправлю тебе слова!")

            print("yo")
            # bit.register_next_step_handler(msg, sender, args=msg.from_user.id)
            asyncio.run(sender(msg.from_user.id))
        else:
            raise BaseException
    except:
        bit.send_message(msg.from_user.id, "Что то не так. Ты точно отправил мне правильное время?")
        bit.register_next_step_handler(msg, add_user)



async def sender(user):

    print(users)
    h = datetime.datetime.now().hour + 5
    m = datetime.datetime.now().minute
    s = datetime.datetime.now().second
    print((users[user] - h * 60 * 60 - m * 60 - s) % (60 * 60 * 24))
    await asyncio.sleep((users[user] - h * 60 * 60 - m * 60 - s) % (60 * 60 * 24))
    print("out")

    while 0 == 0:
        print(h, m, users[user])
        bit.send_message(user, "Привет-привет!\n"
                               "Твои слова на сегодня! Если что - @afder7\n\n" + pick_words())

        # await asyncio.sleep(60 * 60 * 24)
        await asyncio.sleep(10)

bit.polling(none_stop=True, interval=0)
