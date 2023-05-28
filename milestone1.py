from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import *
import logging

#######################################
### REMOVE/CENSOR BEFORE SUBMITTING ###
#######################################
TOKEN: Final = 'TOKEN' 
BOT_USERNAME: Final = '@moneymatetrialbot'
#######################################
### REMOVE/CENSOR BEFORE SUBMITTING ###
#######################################

logging.basicConfig(filename='milestone1.logs', encoding='UTF-8', filemode='w', level=logging.DEBUG, 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

print('Starting up bot...')


#inline keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Add an Expense", callback_data="Add an Expense"),
        ],
        [
            InlineKeyboardButton("Participants", callback_data="Participants"),
        ],
        [
            InlineKeyboardButton("Settle Up", callback_data="Settle Up"),
        ],
        [
            InlineKeyboardButton("Help", callback_data="Help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select what you would like to do today:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    #TO-DO
    await query.edit_message_text(text=f"Selected option: {query.data}")



#create commands

#need to create an account for each group member, need to async across all members?

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Give a description for your expense!')

async def participants_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Select the participants of this expense')

async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('How will you split by?')



#handling the responses

def handle_response(text: str) -> str:
    if isinstance(text, int):
        return "Amount indicated is " + text
    if isinstance(text, str):
        return text

# need to store and update prev accounts

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type
    text: str = str(update.message.text).lower()
    response = ''

    print(f'User({update.message.chat.id} in {message_type} says: "{text}"')

    if message_type == 'group': #when bot is mentioned in the group
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip() #strip remove white spaces at the beginning and the end of the string
            response: str = handle_response(new_text)
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')



def main() -> None:
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    # updater = telegram.ext.Updater(token, use_context=True)
    # dp = updater.dispatcher

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('participants', participants_command))
    app.add_handler(CommandHandler('split', split_command))
    app.add_handler(CallbackQueryHandler(button))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Run bot
    #updater.start_polling(1.0)
    print('Polling...')
    app.run_polling(poll_interval=1.0)
    #updater.idle()


if __name__ == "__main__":
    main()
