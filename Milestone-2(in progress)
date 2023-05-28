from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import logging
logging.basicConfig(filename='milestone1.logs', encoding='UTF-8', filemode='w', level=logging.DEBUG, 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = '5993212456:AAHwV5SlN1BYvLHAGXAi4snjC57bgBjk21w'
BOT_USERNAME = '@moneymadetrialbot'

print('starting up bot...')

#definitions for top level conversation
SELECTING_ACTION, ADD_EXPENSE, VIEW_SUMMARY, SETTLE_UP = map(chr, range(5))
#definitions for second level description conversation
ADDING_EXPENSE_DESCRIPTION, ENTERING_DESCRIPTION = map(chr, range(5,7))
#definitions for third level conversation
ADDING_EXPENSE_AMOUNT, ENTERING_AMOUNT = map(chr, range(7,9))
#definitions for fourth level conversation
ADDING_PARTICIPANTS, DONE = map(chr, range(9,11))
#definitions for fifth level conversation
SELECT_SPLIT, EQUALLY, PERCENTAGES, SPECIFIC_AMOUNTS, SHARES = map(chr, range(11,16))
#definitions for sixth level descriptions conversations
ADDING_VALUE, ENTERING_VALUE = map(chr, range(16,18))
#meta shares
STOPPING, SHOWING = map(chr, range(18,20))
#shortcut for ConversationHandler.END
END = ConversationHandler.END #do we need this since we are just going to the next conversation

#different constants
(
    EXPENSE_DESCRIPTION,
    EXPENSE_AMOUNT,
    START_OVER, #not sure if need this
    VALUES,
    CURRENT_VALUE
) = map(chr, range(20,24))




#top level conversation callbacks: inline keyboard
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "What do you want to do today?"
    )

    keyboard_buttons = [
        [
            InlineKeyboardButton(text="Add an Expense", callback_data=str(ADD_EXPENSE)),
            InlineKeyboardButton(text="View Summary", callback_data=str(VIEW_SUMMARY))
            #InlineKeyboardButton("Participants", callback_data="Participants"),
        ],
        [
            InlineKeyboardButton(text="Settle Up", callback_data=str(VIEW_SUMMARY)),
            #InlineKeyboardButton("Help", callback_data="Help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)
    #await update.message.reply_text("Select what you would like to do today:", reply_markup=reply_markup)

    #if starting over, no need to send a new message
    if context.user_date.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text("MoneyMateBot:")
        await update.message.reply_text(text=text, reply_markup=reply_markup)
    
    context.user_data[START_OVER] = False
    return SELECTING_ACTION


'''async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    #TO-DO
    await query.edit_message_text(text=f"Selected option: {query.data}")'''



#create commands

async def add_expense_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    '''add a description for the created expense'''
    text = "Give a description for your expense!"
    context.user_data[EXPENSE_DESCRIPTION] = update.callback_query.data
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=text)

    return ENTERING_DESCRIPTION

async def save_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    ''''Save input for the expense description'''
    user_data = context.user_data
    user_data[EXPENSE_DESCRIPTION] = update.message.text
    return ADDING_EXPENSE_AMOUNT

async def add_expense_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    '''specify the amount for the created expense'''
    text = "Add the expense amount!"
    context.user_data[EXPENSE_AMOUNT] = update.callback_query.data
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=text)

    return ENTERING_AMOUNT

async def save_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    ''''Save input for the expense description'''
    user_data = context.user_data
    user_data[EXPENSE_DESCRIPTION] = update.message.text
    return ADDING_EXPENSE_AMOUNT

async def add_participants(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    '''select participants involved in this expense'''
    keyboard_buttons = [
        #[
        #    InlineKeyboardButton(text="UserID1", callback_data="USERID1"),
        #    InlineKeyboardButton(text="UserID2", callback_data="USERID2")
        #],
        #[
        #    InlineKeyboardButton(text="UserID3", callback_data="USERID4"),
        #    InlineKeyboardButton(text="UserID3", callback_data="USERID4")
        #],
        [
            InlineKeyboardButton(text="Add Participant", callback_data=str(DONE))
            InlineKeyboardButton(text="Done", callback_data=str(DONE))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    if not context.user_data.get(DONE):
        text = "Please add the participants of this expense." #current participants are:
        query = update.callback_query

        await update.query.answer()
        await update.query.edit_message_text(text = text, reply_markup=reply_markup)
    else:
        text = "Participants added. Participants are: ..."
        await update.query.edit_message_text(text = text, reply_markup=reply_markup)
        context.user_data[DONE] = True #not sure about this, how do they indicate done
    return ADDING_PARTICIPANTS



async def split_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    keyboard_buttons = [
        [
            InlineKeyboardButton(text="Equally", callback_data=str(EQUALLY)),
            InlineKeyboardButton(text="Percentages", callback_data=str(PERCENTAGES))
        ],
        [
            InlineKeyboardButton(text="Specific Amounts", callback_data=str(SPECIFIC_AMOUNTS)),
            InlineKeyboardButton(text="Shares", callback_data=str(SHARES))
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)

    return SELECT_SPLIT

async def specify_value(update:Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    '''specify the value of splitting for the created expense'''
    text = "How is it split by?"
    context.user_data[VALUES] = update.callback_query.data
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=text)

    return ENTERING_VALUE

async def end_describing(update: Update, context: ContextTypes) -> int:
    '''End gathering of values and return to parent conversation.'''
    user_data = context.user_data

async def save_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    ''''Save input for the split'''
    user_data = context.user_data
    user_data[VALUES] = update.message.text
    return ADDING_VALUE

'''to show current expense'''

async def stop_nexted(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str: #to cancel entering the expense?
    '''Completley end conversation from within nested conversation.'''
    await update.message.reply_text("Okay, bye.")

    return STOPPING


#async def expense_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text('Give a description for your expense!')

#async def participants_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text('Select the participants of this expense')

#async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text('How will you split by?')

#async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("Here is a summary:")

#async def settle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("To settle up:")



#handling the responses

'''def handle_response(text: str) -> str:
#     if isinstance(text, int):
#         return "Amount indicated is " + text
#     if isinstance(text, str):
    return text'''

'''async def enter_expense_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data"""
    context.user_data[EXPENSE_NAME]'''


'''async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = str(update.message.text).lower()
    response = ''

    print(f'User({update.message.chat.id} in {message_type} says: "{text}"')

    if message_type == 'group': #when bot is mentioned in the group
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip() #strip remove white spaces at the beginning and the end of the string
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)'''



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')



def main() -> None:
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    #ConversationHandler - splitting amount
    split_amt_description = ConversationHandler(
        entry_points = [
            CallbackQueryHandler(
                split_amount, pattern="^" + str(EQUALLY) + "$|^" + str(PERCENTAGES) + "$|^" + str(SPECIFIC_AMOUNTS) + "$|^" + str(SHARES) + "$"                                                                                                                  
            )
        ],
        states={
            SELECT_SPLIT: [
                CallbackQueryHandler(specify_value, pattern="^?!" + str(END) + ").*$")
            ],
            ENTERING_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_value)],
            },
            fallbacks=[
                CallbackQueryHandler()
            ],
            map_to_parent={
                #after showing data
                SHOWING: SHOWING,
            }

    )

    #ConversationHandler - Select Participants
    










    '''#Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('participants', participants_command))
    app.add_handler(CommandHandler('split', split_command))
    app.add_handler(CommandHandler('summary', summary_command))
    app.add_handler(CommandHandler('settle', settle_command))
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
    main()'''
