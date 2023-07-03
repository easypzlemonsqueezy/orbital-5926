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
from typing import Final, Any, Dict, Tuple

logging.basicConfig(filename='milestone1.logs', encoding='UTF-8', filemode='w', level=logging.DEBUG, 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TOKEN = '5993212456:AAHwV5SlN1BYvLHAGXAi4snjC57bgBjk21w'
BOT_USERNAME = '@moneymadetrialbot'

SELECTING_ACTION, ADD_EXPENSE, VIEW_SUMMARY, SETTLE_UP = map(chr,range(4))

ENTER_EXPENSE_DETAILS, ENTERING, CONTINUE_TO_PART = map(chr, range(4,7))

ADD_PARTICIPANTS, ADDING_PARTICIPANTS, ADDING = map(chr, range(7,10))

STOPPING, SHOWING = map(chr,range(10,12))

END = ConversationHandler.END   

(
     EXPENSES, #EXPENSE ID
     EXPENSE_DETAILS,
     EXPENSE_DESC,
     EXPENSE_AMT,
     PARTICIPANTS,
     START_OVER
) =map(chr,range(12,18))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "What do you want to do today?"
    buttons = [
        [
            InlineKeyboardButton(text="Add Expense", callback_data=str(ADD_EXPENSE)),
            InlineKeyboardButton(text="View Summary", callback_data=str(VIEW_SUMMARY)),
        ],
        [
            InlineKeyboardButton(text="Settle Up", callback_data=str(SETTLE_UP)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(
            "Hi, I'm MoneyMate and I'm here to help you gather track your group expenses."
        )
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION



async def expense_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Enter your expense details"
    buttons = [
        [
            InlineKeyboardButton(text="Expense Description", callback_data=str(EXPENSE_DESC)),
            InlineKeyboardButton(text="Expense Amount", callback_data=str(EXPENSE_AMT))
        ],
        [
            InlineKeyboardButton(text="Continue to Participants", callback_data=str(CONTINUE_TO_PART)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    #for a new entry, create new empty dictionary of expenses
    if not context.user_data.get(START_OVER):
        context.user_data[EXPENSES] = {}
        text = "Please select a feature to update."

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = "Got it! Please select a feature to update."
        await update.message.reply_text(text=text, reply_markup=keyboard)   

    context.user_data[START_OVER] = False
    return ENTER_EXPENSE_DETAILS



async def enter_expense_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected detail."""
    context.user_data[EXPENSE_DETAILS] = update.callback_query.data
    text = "Okay, tell me."

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

    return ENTERING



async def save_expense_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save current detail and return to detail selection."""
    user_data = context.user_data
    user_data[EXPENSES][user_data[EXPENSE_DETAILS]] = update.message.text

    user_data[START_OVER] = True
    return await expense_details(update, context)



async def participants(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            InlineKeyboardButton(text="Add Participants", callback_data=str(ADD_PARTICIPANTS)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    #if no participants yet, create empty list of participants
    if not context.user.get(START_OVER):
        context.user_data[PARTICIPANTS] = []
        text = "Please add participants."

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    
    else:
        ls = context.user_data[PARTICIPANTS]
        text = "Got it! Press Done once all participants have been added."
        #for i in ls:
        #    text += f"{i}\n"
        await update.message.reply_text(text=text, reply_markup=keyboard)
    
    context.user_data[START_OVER] = False
    return ADDING_PARTICIPANTS



async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Add Name"

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

    return ADDING


async def save_participant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[PARTICIPANTS].append(update.message.text)

    user_data[START_OVER] = True

    return await participants(update, context)



async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

    ls = user_data[PARTICIPANTS]
    str = ""
    for i in ls:
        str += f"{i}\n"

    user_data = context.user_data
    text = f"Expense Description: {user_data[EXPENSES][EXPENSE_DESC]}"
    text += f"Expense Amount: {user_data[EXPENSES][EXPENSE_AMT]}"
    #text += f"Participants: \n{str}"

    await update.message.reply_text("text")
    return SHOWING


async def settle_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data[START_OVER] = True
    await update.message.reply_text("Settle Up!")
    return STOPPING

async def end_conv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await start(update,context)
    return STOPPING


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text("Okay, bye.")

    return END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()


    part_convo = ConversationHandler(
        entry_points=[CallbackQueryHandler(participants, pattern="^" + str(CONTINUE_TO_PART) + "$")],
        states={
            ADDING_PARTICIPANTS: [CallbackQueryHandler(enter_name, pattern="^(?!" + str(ADD_PARTICIPANTS) + ").*$")],
            ADDING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_participant)],
        
        },
        fallbacks=[
            CallbackQueryHandler(end_conv, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop)
        ],
        map_to_parent={
            END: SELECTING_ACTION,
            STOPPING: STOPPING
        }
    )


    exp_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(expense_details, pattern="^" + str(ADD_EXPENSE) + "$")],
        states={
            ENTER_EXPENSE_DETAILS: [
                CallbackQueryHandler(enter_expense_details, pattern=f"^{EXPENSE_DESC}$|^{EXPENSE_AMT}$")],
            ENTERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, 
            save_expense_details)],
            CONTINUE_TO_PART: [part_convo],
        },
        fallbacks=[
            CommandHandler("stop", stop),
        ],
        map_to_parent={
            STOPPING: STOPPING,
        },
    )

    selection_handlers = [
        exp_conv,
        CallbackQueryHandler(show_data, pattern="^" + str(VIEW_SUMMARY) + "$"),
        CallbackQueryHandler(settle_up, pattern="^" + str(SETTLE_UP) + "$"),
        CallbackQueryHandler(end_conv, pattern="^" + str(END) + "$"),
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states = {SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            SELECTING_ACTION: [exp_conv],
            ADD_EXPENSE: selection_handlers,
            VIEW_SUMMARY: selection_handlers,
            CONTINUE_TO_PART: [part_convo],
            SETTLE_UP: [CommandHandler("stop",stop)],
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
