import prompt
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler

import credentials
from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu,
                  default_callback_handler, load_prompt, send_text_buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'random': 'Дізнатися випадковий цікавий факт 🧠',
        'gpt': 'Задати питання чату GPT 🤖',
        'talk': 'Поговорити з відомою особистістю 👤',
        'quiz': 'Взяти участь у квізі ❓'
        # Додати команду в меню можна так:
        # 'command': 'button text'

    })
async def randomm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt_text = load_prompt('random')
    chat_gpt.set_prompt(prompt_text)
    response = await chat_gpt.send_message_list()
    await send_image(update, context, 'random')
    await send_text(update, context, response)
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, name='random')
    text = load_message('random')
    await send_text(update, context, text)

    prompt = load_prompt('random')

    #chat_gpt.set_prompt(prompt)
    answer = await chat_gpt.send_question(prompt, "Дай факт")
    #await send_text(update, context, answer)
    await send_text_buttons(update, context, answer, {"random_end": "Закінчити",
                                                      "random_more": "Хочу ще факт"})

async def random_buttons_query_handler(update: Update, context: CallbackQueryHandler):
    if update.callback_query:
        return
    if update.callback_query.data == "random_end":
        await start(update, context)
    elif update.callback_query.data == "random_more":
        await random(update, context)

chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.TG_TOKEN).build()

# Зареєструвати обробник команди можна так:
# app.add_handler(CommandHandler('command', handler_func))
app.add_handler(CommandHandler('start', start))

app.add_handler(CommandHandler('random', random))
# Зареєструвати обробник колбеку можна так:
app.add_handler(CallbackQueryHandler(random_buttons_query_handler, pattern='^app_.*'))
#app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
