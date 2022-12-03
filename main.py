#import task as task
import telebot
from telebot import types  # для указание типов
from sql import *

token = '5788012378:AAF8dcEhkN7KSV0S-IN_AZoLOscH7eVOtLc'
# ссылка на бота https://t.me/Homelessness_bot
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем 3 кнопки в меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить задачу")
    btn2 = types.KeyboardButton("Твои задачи на день")
    btn3 = types.KeyboardButton("Удалить задачу")
    markup.add(btn1, btn2, btn3)
    bot.send_message(m.chat.id,
                     'Привет. Жизнь это игра. И твоя цель не стать бомжом. Поэтому выполняй задачи вовремя. Удачи',
                     reply_markup=markup)


user_task = [] #тут мы храним список задач
call_task = [] #тут храним счетчит задач



@bot.message_handler(content_types=['text'])
def start(m):
    if m.text.strip() == "Добавить задачу":
        mesg = bot.send_message(m.chat.id, 'Please send me message')
        bot.register_next_step_handler(mesg, do_task) # переходим к функции, которая добавляет задачу в SQL
    if m.text.strip() == "Твои задачи на день":
        markup = types.InlineKeyboardMarkup()
        us = m.from_user.username # берем юзернейм, потому нужно брать задачи для отдельных пользователей
        #print(us)
        k = cursor.execute("""
                SELECT task 
                FROM taskbase""").fetchall() # берем все задачи из базы
        #print(k)
        new5 = [] # записываем отформатированные задачи
        caal = [] # записываем счетчик задач
        numb = 1 # счетчик callback_data
        for kll in k:
            new = str(kll)
            # форматирование
            new1 = new.replace("'","")
            new2 = new1.replace("(","")
            new3 = new2.replace(")","")
            new4 = new3.replace(",","")
            new5.append(new4)

            point = types.InlineKeyboardButton(text=(new4), callback_data=numb)
            markup.add(point)
            caal.append(numb) # добавляем в список caal наш счетчик
            numb += 1 # увеличиваем счетчик
        user_task = new5 # итоговый счисок задач
        call_task = caal # итоговый список количества задач
        print(user_task, call_task)
        bot.send_message(m.chat.id, "Твои задачи на день", reply_markup=markup)
        #bot.register_next_step_handler(mesg, taskforday())

# эта часть call не доработана
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    #if call.data == call_task[0]:
     #   print(user_task[0])
      #  markup = types.InlineKeyboardMarkup()
       # delete = types.InlineKeyboardButton(text="Выполнить", callback_data='l')
        #markup.add(delete)
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          #    text="Что хочешь сделать?", reply_markup=markup)
    if call.data == 'o':
        print('d')
    else:
        len_task = len(call_task)
        for i in range(len_task):
            print('t')
            if call.data == call_task[i]:
                print(i)
                print(user_task[i])
            else:
                break

#добавление задачи в базу данных
def do_task(m):
    bot.send_message(m.chat.id, 'Задача добавлена')
    # в базу данных попадает юзернейм и задача
    username = m.from_user.username
    task = m.text

    db_table_val(username=username, task=task)


bot.polling(none_stop=True, interval=0)

# if __name__ == '__main__':
#    bot.polling()
