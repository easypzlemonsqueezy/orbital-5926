"""
KNOWN LIMITATIONS OF MONEYMATE:
1. MoneyMate can only handle the case of 1 payee per expense.
2. MoneyMate can only handle expenses in one currency, the current version is coded in SGD.
"""

import telebot
from telebot import types

TOKEN = "6625167658:AAHs-5VBxm89Y6Tc29fHlSjGXTpBLySRxeE"
BOT_USERNAME = '@MoneyMate5926bot'

bot = telebot.TeleBot(TOKEN)

expenses = {}

##################################
### list of available commands ###
##################################
commands = {
    'start' : 'Starts MoneyMate',
    'help' : 'Provides information on the list of commands available for MoneyMate',
    'reset' : 'Resets MoneyMate',
}

####################
### help command ###
####################
@bot.message_handler(commands=['help'])
def help_command(message):
    text = "The following commands are available: \n"
    for command in commands:
        text += "/" + command + ": "
        text += commands[command] + "\n"
    bot.send_message(message.chat.id, text)

#######################
### helper commands ###
#######################
def start_command_markup():
    markup = types.ReplyKeyboardMarkup()
    add_expense = types.KeyboardButton('Add an Expense')
    view_summary = types.KeyboardButton('View Expenses Summary')
    view_balance = types.KeyboardButton('View Balance')
    view_participants = types.KeyboardButton('View Participants')
    reset = types.KeyboardButton('Reset Expenses and Balance')
    markup.row(add_expense)
    markup.row(view_summary)
    markup.row(view_balance)
    markup.row(view_participants)
    markup.row(reset)
    return markup

@bot.message_handler(func=lambda message: message.entities is not None and any(entity.type == 'bot_command' for entity in message.entities))
def handle_commands(message):
    # Extract the command
    command_text = message.text.split(' ', 1)[0]
    command = command_text[1:]  # Remove the slash '/' from the command

    # Process the command
    if command == 'start':
        start_command(message)
    elif command == 'help':
        help_command(message)
    elif command == 'reset':
        reset_command(message)

############################################
### start command and alt-start commands ###
############################################
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id not in expenses:
        expenses[user_id] = []
    bot.send_message(user_id, "Hi! I'm MoneyMate and I'm here to help you gather and track your group expenses.")
    help_command(message)
    bot.send_message(user_id, "What would you like to do today?", reply_markup=start_command_markup())

def alt_start_command(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "What else would you like to do today?", reply_markup=start_command_markup())

def exception_to_start_command(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "What would you like to do today?", reply_markup=start_command_markup())

##############################
### add an expense command ###
##############################
@bot.message_handler(func=lambda message: message.text == "Add an Expense")
def add_expense_description_command(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(user_id, 'Enter the description for the expense:', reply_markup=markup)
    bot.register_next_step_handler(message, add_expense_amount_command)

def add_expense_amount_command(message):
    user_id = message.from_user.id
    try:
        description = message.text

        bot.send_message(user_id, 'Enter the amount for the expense (e.g. 12.34):')
        bot.register_next_step_handler(message, add_payee_command, user_id, description)
    except Exception:
        bot.reply_to(message, 'Invalid input. Please press the "Add an Expense" button to start again.')
        exception_to_start_command(message)

def add_payee_command(message, user_id, description):
    user_id = message.from_user.id
    try:
        total_amount = float(message.text.replace('$', ''))
        bot.send_message(user_id, 'Enter the payee for the expense:\nNote: There should only be one payee per expense.')
        bot.register_next_step_handler(message, add_participants_command, user_id, description, total_amount)
    except Exception:
        bot.reply_to(
            message,
            'Invalid amount format. Please input a number or a decimal (e.g. 12.34).\n'
            'Please press the "Add an Expense" button to start again.')
        exception_to_start_command(message)

def add_participants_command(message, user_id, description, total_amount):
    user_id = message.from_user.id
    try:
        payee = message.text.strip().lower()

        expenses[user_id].append({
            'payee': payee,
            'participants': [],
            'total_amount': total_amount,
            'description': description
        })

        bot.send_message(user_id, 'Enter the participants involved in this expense, separated by commas, in this format:\n'
                         f'PZ, Dionne, Ivan, ...')
        bot.register_next_step_handler(message, split_type_command, user_id)
    except Exception:
        bot.reply_to(message, 'Invalid input. Please press the "Add an Expense" button to start again.')
        exception_to_start_command(message)

def split_type_command(message, user_id):
    user_id = message.from_user.id
    try:
        participants = message.text.strip().lower().split(',')
        participants = [participant.strip() for participant in participants]

        # Store the participants in the user's context
        current_expense = expenses[user_id][-1]
        current_expense['participants'] = participants

        markup = types.ReplyKeyboardMarkup()
        equal_button = types.KeyboardButton('Equally')
        unequal_button = types.KeyboardButton('Unequally')
        markup.row(equal_button)
        markup.row(unequal_button)
        bot.send_message(user_id, 'How do you wish to split this expense? (Equally/Unequally):', reply_markup=markup)
        bot.register_next_step_handler(message, save_expense_equal_command, user_id)
    except Exception:
        bot.send_message(
            user_id,
            'Invalid input. Please enter the participants with comma-separated names.\n'
            'Please press the "Add an Expense" button to start again.'
        )
        exception_to_start_command(message)

def save_expense_equal_command(message, user_id):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardRemove(selective=False)
    try:
        split_type = message.text.strip().lower()
        if split_type not in ('equally', 'unequally'):
            raise ValueError

        # Get participants and total amount from the user's context
        current_expense = expenses[user_id][-1]
        payee = current_expense['payee']
        participants = current_expense['participants']
        total_amount = current_expense['total_amount']

        # Calculate the amount for each participant based on equal split
        # If the split is unequal, pass it to save_expense_unequal_command
        if split_type == 'equally': # Equal split
            equal_amount_per_participant = total_amount / len(participants)
            # Store the expense with equal split in the dictionary
            current_expense['equal_amount_per_participant'] = equal_amount_per_participant
        else:  # Unequal split
            bot.send_message(
                user_id,
                'Enter the amount of the expense for each participant in the order keyed above, separated by commas\n'
                '(e.g. 6, 4, 2.34):\n'
                'Note: Sum of amounts should add up to the total amount of the expense.', reply_markup=markup)
            bot.register_next_step_handler(message, save_expense_unequal_command, user_id, participants, total_amount)
            return

        bot.send_message(
            user_id,
            f'Expense of SGD {total_amount:.2f} for "{current_expense["description"]}" added with \n'
            f'Participants: {", ".join(participants)} \n'
            f'Payee: {payee}',
            reply_markup=markup
        )
        alt_start_command(message)
    except Exception:
        bot.reply_to(message,
                     'Invalid input. Please enter "Equally" or "Unequally" as the split type.\n'
                     'Please press the "Add an Expense" button to start again.')
        exception_to_start_command(message)
    # print(expenses)

def save_expense_unequal_command(message, user_id, participants, total_amount):
    user_id = message.from_user.id
    try:
        amounts = message.text.replace('$', '').split(',')
        unequal_amount_per_participant = [float(amount) for amount in amounts]

        if len(unequal_amount_per_participant) != len(participants) or sum(unequal_amount_per_participant) != total_amount:
            raise ValueError

        # Store the expense with unequal split in the dictionary
        current_expense = expenses[user_id][-1]
        current_expense['unequal_amount_per_participant'] = unequal_amount_per_participant
        payee = current_expense['payee']

        bot.send_message(
            user_id,
            f'Expense of SGD {total_amount:.2f} for "{current_expense["description"]}" added with \n'
            f'Participants: {", ".join(participants)} \n'
            f'Payee: {payee}'
        )
        alt_start_command(message)
    except Exception:
        bot.reply_to(message,
                     f'Invalid input. Please enter {len(participants)} amounts separated by commas'
                     'or make sure the amounts add up to the total amount.\n'
                     'Please press the "Add an Expense" button to start again.')
        exception_to_start_command(message)

#################################
### view participants command ###
#################################
@bot.message_handler(func=lambda message: message.text == "View Participants")
def view_participants_command(message):
    user_id = message.from_user.id

    if expenses[user_id] == []:
        bot.reply_to(message, 'You have no recorded participants.')
    else: #if user_id in expenses
        participants_set = set()
        for expense in expenses[user_id]:
            participants = expense['participants'] + [expense['payee']]
            participants_set.update(participants)
        bot.reply_to(message, f'Participants: {", ".join(participants_set)}')

    alt_start_command(message)

############################
### view summary command ###
############################
@bot.message_handler(func=lambda message: message.text == "View Expenses Summary")
def view_summary_command(message):
    user_id = message.from_user.id

    if expenses[user_id] == []:
        bot.reply_to(message, 'You have no recorded expenses.')
    else: #if user_id in expenses
        # Preparatory calculations of the response
        response = 'Summary of Expenses:\n'
        expenses_by_participant = {}
        total_expenses_by_participant = {}
        total_expenses = 0

        for expense in expenses[user_id]:
            participants = expense['participants']
            total_amount = expense['total_amount']
            description = expense['description']

            if 'equal_amount_per_participant' in expense:  # Equal split
                equal_amount_per_participant = expense['equal_amount_per_participant']
                response += f'-> SGD {total_amount:.2f} for "{description}"\n'

                for participant in participants:
                    if participant not in expenses_by_participant:
                        expenses_by_participant[participant] = []
                    expenses_by_participant[participant].append(
                        f'Your share for "{description}": SGD {equal_amount_per_participant:.2f}'
                    )
                    if participant not in total_expenses_by_participant:
                        total_expenses_by_participant[participant] = 0
                    total_expenses_by_participant[participant] += equal_amount_per_participant

                total_expenses += total_amount

            elif 'unequal_amount_per_participant' in expense:  # Unequal split
                unequal_amount_per_participant = expense['unequal_amount_per_participant']
                response += f'-> SGD {total_amount:.2f} for "{description}"\n'

                for participant, amount in zip(participants, unequal_amount_per_participant):
                    if participant not in expenses_by_participant:
                        expenses_by_participant[participant] = []
                    expenses_by_participant[participant].append(
                        f'Your share for "{description}": SGD {amount:.2f}'
                    )
                    if participant not in total_expenses_by_participant:
                        total_expenses_by_participant[participant] = 0
                    total_expenses_by_participant[participant] += amount

                total_expenses += total_amount

        # Formatting the response with grouped expenses and total expenses
        response += f'Total Group Expenses: SGD {total_expenses:.2f}\n\n'
        for participant, participant_expenses in expenses_by_participant.items():
            response += f'Expenses for {participant}:\n'
            response += '\n'.join(participant_expenses)
            response += f'\nTotal Expenses for {participant}: SGD {total_expenses_by_participant[participant]:.2f}\n\n'

        bot.reply_to(message, response)

    alt_start_command(message)

############################
### view balance command ###
############################
@bot.message_handler(func=lambda message: message.text == "View Balance")
def view_balance_command(message):
    user_id = message.from_user.id

    if expenses[user_id] == []:
        bot.reply_to(message, 'You have no recorded expenses.')
    else: #if user_id in expenses
        # Preparatory calculations of the response
        response = 'Balance Across Expenses:\n\n'
        balance_by_participant = {}
        total_group_expenses = 0

        for expense in expenses[user_id]:
            participants = expense['participants']
            total_amount = expense['total_amount']
            payee = expense['payee']

            if 'equal_amount_per_participant' in expense:  # Equal split
                equal_amount_per_participant = expense['equal_amount_per_participant']
                for participant in participants:
                    if participant not in balance_by_participant:
                        balance_by_participant[participant] = 0
                    balance_by_participant[participant] -= equal_amount_per_participant
                if payee not in balance_by_participant:
                    balance_by_participant[payee] = 0
                balance_by_participant[payee] += total_amount
                total_group_expenses += total_amount
            elif 'unequal_amount_per_participant' in expense:  # Unequal split
                unequal_amount_per_participant = expense['unequal_amount_per_participant']
                for participant, amount in zip(participants, unequal_amount_per_participant):
                    if participant not in balance_by_participant:
                        balance_by_participant[participant] = 0
                    balance_by_participant[participant] -= amount
                if payee not in balance_by_participant:
                    balance_by_participant[payee] = 0
                balance_by_participant[payee] += total_amount
                total_group_expenses += total_amount

        # Formatting the balances for each participant in the response
        for participant, balance_amount in balance_by_participant.items():
            response += f'{participant}: SGD {balance_amount:.2f}\n'
        response += '\nNote: \nA positive balance of $x means you are being owed $x '
        response += 'while a negative balance of $x means you owe $x'

        bot.reply_to(message, response)

    alt_start_command(message)

#####################
### reset command ###
#####################
@bot.message_handler(commands=['reset'])
@bot.message_handler(func=lambda message: message.text == "Reset Expenses and Balance")
def reset_command(message):
    user_id = message.from_user.id
    for user_id in expenses:
        expenses[user_id] = []
    bot.send_message(user_id, 'MoneyMate has been reset.')
    alt_start_command(message)

#########################
### catch-all command ###
#########################
@bot.message_handler(func=lambda message: True)
def catchall_command(message):
    bot.reply_to(message, 'Invalid input. Please select an option using the keyboard.')
    exception_to_start_command(message)

######################
### starts the bot ###
######################
bot.infinity_polling()

while True: # Don't end the main thread
    pass
