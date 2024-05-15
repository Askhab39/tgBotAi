import telebot # type: ignore
from openai import OpenAI # type: ignore

client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

bot = telebot.TeleBot("6842173277:AAGZ-1pima774AdQ11luGahbdSsS_pORp2I")

chat_histories = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может общаться с помощью нейронной сети. Просто напиши мне что-нибудь.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    user_id = message.chat.id
    user_message = message.text

    messages = chat_histories.get(user_id, [])
    messages.append({"role": "user", "content": user_message})

    bot.send_message(user_id, "Генерирую ответ...")

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", 
        messages=messages
    )

    ai_message = chat_completion.choices[0].message.content

    # Отправляем ответ и скрываем сообщение "Генерирую ответ..."
    bot.edit_message_text(chat_id=user_id, message_id=message.message_id + 1, text=ai_message)

    messages.append({"role": "assistant", "content": ai_message})
    chat_histories[user_id] = messages

bot.polling()