import os
import telebot as tb
import services as svc
import keyboards as kb
import database as db
from typing import List
from settings import BOT_TOKEN
from telebot.types import InlineKeyboardButton


bot = tb.telebot.TeleBot(BOT_TOKEN)

if not os.path.exists('./data'):
    os.mkdir('./data')

conn = db.create_connection('./data/settings.db')
cursor = db.create_cursor(conn)
db.create_table(
            cursor, 
            'settings', 
            [
            'id INTEGER PRIMARY KEY AUTOINCREMENT', 
            'user_id INT', 
            'pagination_status TEXT'
            ]
        )

def bot_pln_msg(bot: tb.TeleBot, call: tb.types.CallbackQuery) -> None:
        """Sends PLN news message to user.

        Args:
            bot (tb.TeleBot): Bot instance.
            call (tb.types.CallbackQuery): CallbackQuery instance.
        Returns: None
        """
        bot.send_message(
            call.message.chat.id,
            """
Press *'Today'* to get today's news
Press *'Accidents'* to get news about accidents
Press *'Automir'* to get news about automir
Press *'Culture'* to get news about culture
Press *'Society'* to get news about society
Press *'Back'* to get back to main menu
            """,
            parse_mode='MarkdownV2',
            reply_markup=kb.get_pln_inline_markup(),
        )

def bot_cdi_msg(bot: tb.TeleBot, call: tb.types.CallbackQuery) -> None:
        """Sends CDI news message to user.

        Args:
            bot (tb.TeleBot): Bot instance.
            call (tb.types.CallbackQuery): CallbackQuery instance.
        Returns: None
        """
        bot.send_message(
            call.message.chat.id,
            """
Press *'News'* to get latest news
Press *'Market'* to get regional market news
Press *'Business'* to get regional business news
Press *'Rabota'* to get info about vacancies
Press *'Back'* to get back to main menu
            """,
            parse_mode='MarkdownV2',
            reply_markup=kb.get_cdi_inline_markup(),
        )

def bot_ipsk_msg(bot: tb.TeleBot, call: tb.types.CallbackQuery) -> None:
        """Sends IPSK news message to user.

        Args:
            bot (tb.TeleBot): Bot instance.
            call (tb.types.CallbackQuery): CallbackQuery instance.
        Returns: None
        """
        bot.send_message(
            call.message.chat.id,
            """
Press *'News'* to get latest news
Press *'Back'* to get back to main menu
            """,
            parse_mode='MarkdownV2',
            reply_markup=kb.get_ipsk_inline_markup(),
        )

def bot_back_msg(bot: tb.TeleBot, call: tb.types.CallbackQuery) -> None:
        """Sends main menu message to user.

        Args:
            bot (tb.TeleBot): Bot instance.
            call (tb.types.CallbackQuery): CallbackQuery instance.
        Returns: None
        """
        bot.send_message(
            call.message.chat.id,
            "Please choose an option:",
            parse_mode='MarkdownV2',
            reply_markup=kb.get_main_inline_markup(),
        )

def bot_settings_msg(bot: tb.TeleBot, call: tb.types.CallbackQuery) -> None:
        """Sends settings message to user.

        Args:
            bot (tb.TeleBot): Bot instance.
            call (tb.types.CallbackQuery): CallbackQuery instance.
        Returns: None
        """
        bot.send_message(
            call.message.chat.id,
            """
Press *'Show all list'* to get all news list
Press *'Use Pagination'* to use pagination
Press *'Back'* to get back to main menu
            """,
            parse_mode='MarkdownV2',
            reply_markup=kb.get_settings_inline_markup(),
        )

def delete_past_messages(
        bot: tb.TeleBot, 
        call: tb.types.CallbackQuery, 
        quantity: int = 10) -> None:
    """Deletes past messages.

    Args:
        bot (tb.TeleBot): Bot instance.
        call (tb.types.CallbackQuery): CallbackQuery instance.
        quantity (int, optional): Quantity of messages to delete. Defaults to 10.
    Returns: None
    """
    for i in range(quantity):
        try:
            bot.delete_message(
                call.message.chat.id, 
                call.message.message_id - i)
        except tb.apihelper.ApiTelegramException:
            break

def get_formatted_news(news: List[List[str]]) -> List[str]:
    """Formats news list to be sent to user.

    Args:
        news (List[List[str]]): List of news.
    Returns:
        List[str]: Formatted news list.
    """
    return [
            f"Date: {item[0]}\nTitle: {item[1]}\nLink: {item[2]}" 
            for item in news
        ]

def send_news_page(
        bot: tb.TeleBot,
        msg: tb.types.Message, 
        news: List[str], 
        page: int=1, 
        _type: str=None) -> None:
    """Sends news page to user and adds pagination buttons to it.

    Args:
        bot (tb.TeleBot): Bot instance.
        msg (tb.types.Message): Message instance.
        news (List[str]): List of news.
        page (int, optional): Page number. Defaults to 1.
        _type (str, optional): Type of news. Defaults to None.
    Returns: None
    """
    pagination = kb.InlineKeyboardPaginator(
        len(news),
        current_page=page,
        data_pattern='number#{page}'+f'#{_type}')
    pagination.add_after(InlineKeyboardButton('Back', callback_data='back'))
    bot.send_message(
        msg.chat.id,
        news[page-1],
        reply_markup=pagination.markup,
        parse_mode='Markdown'
    )

def handle_main_callback_query(
        bot: tb.TeleBot, 
        call: tb.types.CallbackQuery) -> None:
    """Handles main menu callback query.

    Args:
        bot (tb.TeleBot): Bot instance.
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    if call.data == "pln":
        bot_pln_msg(bot, call)
        return
    if call.data == "cdi":
        bot_cdi_msg(bot, call)
        return
    if call.data == "ipsk":
        bot_ipsk_msg(bot, call)
        return
    if call.data == "settings":
        bot_settings_msg(bot, call)
        return
    if call.data == "back":
        bot_back_msg(bot, call)
        return

def handle_settings(bot: tb.TeleBot, call: tb.types.CallbackQuery) -> None:
    """Handles settings callback query.

    Args:
        bot (tb.TeleBot): Bot instance.
        call (tb.types.CallbackQuery): CallbackQuery instance.
    Returns: None
    """
    if call.data in ['pagination_on', 'pagination_off']:
        db.insert_data(
            conn, 
            cursor, 
            'settings', 
            (call.from_user.id, call.data))
        bot_back_msg(bot, call)

def send_all_news(
          bot: tb.TeleBot, 
          call: tb.types.CallbackQuery, 
          news: list) -> None:
    for date, title, link in news[::-1]:
        bot.send_message(
            call.message.chat.id, 
            f"Date: {date}\nTitle: {title}\nLink: {link}",
            parse_mode='html'
            )

def handle_pln_callback_query(call: tb.types.CallbackQuery) -> None:
    """Handles PLN callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    try:
        pagination_status = db.select_pagination_status(
            cursor, 
            call.from_user.id)[0][0]

        if pagination_status == 'pagination_on':
            news = get_formatted_news(svc.get_pln_news(call.data)[call.data])
            send_news_page(bot, call.message, news, _type=call.data)
        else: 
            send_all_news(bot, call, svc.get_pln_news(call.data)[call.data])
            bot_pln_msg(bot, call)
    except Exception as e:
        bot.send_message(
            call.message.chat.id, 
            f"Error: {e}"
            )

def handle_cdi_callback_query(call: tb.types.CallbackQuery) -> None:
    """Handles CDI callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    try:
        pagination_status = db.select_pagination_status(
            cursor, 
            call.from_user.id)[0][0]

        if  pagination_status == 'pagination_on':
            news = get_formatted_news(svc.get_cdi_news(call.data)[call.data])
            send_news_page(bot, call.message, news, _type=call.data)
        else: 
            send_all_news(bot, call, svc.get_cdi_news(call.data)[call.data])
            bot_pln_msg(bot, call)
    except Exception as e:
        bot.send_message(
            call.message.chat.id, 
            f"Error: {e}"
            )

def handle_ipsk_callback_query(call: tb.types.CallbackQuery) -> None:
    """Handles IPSK callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    try:
        pagination_status = db.select_pagination_status(
            cursor, 
            call.from_user.id)[0][0]

        if pagination_status == 'pagination_on':
            news = get_formatted_news(svc.get_ipsk_news(call.data)[call.data])
            send_news_page(bot, call.message, news, _type=call.data)
        else: 
            send_all_news(bot, call, svc.get_ipsk_news(call.data)[call.data])
            bot_pln_msg(bot, call)
    except Exception as e:
        bot.send_message(
            call.message.chat.id, 
            f"Error: {e}"
            )

def handle_pln_pagination(call: tb.types.CallbackQuery) -> None:
    """Handles PLN pagination callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    try:
        category = call.data.split('#')[2]
        page = int(call.data.split('#')[1])
        news = get_formatted_news(svc.get_pln_news(category)[category])
        send_news_page(bot, call.message, news, page, _type=category)
    except Exception as e:
        bot.send_message(
            call.message.chat.id, 
            f"Error: {e}"
            )

def handle_cdi_pagination(call: tb.types.CallbackQuery) -> None:
    """Handles CDI pagination callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    try:
        category = call.data.split('#')[2]
        page = int(call.data.split('#')[1])
        news = get_formatted_news(svc.get_cdi_news(category)[category])
        send_news_page(bot, call.message, news, page, _type=category)
    except Exception as e:
        bot.send_message(
            call.message.chat.id, 
            f"Error: {e}"
            )

def handle_ipsk_pagination(call: tb.types.CallbackQuery) -> None:
    """Handles IPSK pagination callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
    try:
        category = call.data.split('#')[2]
        page = int(call.data.split('#')[1])
        news = get_formatted_news(svc.get_ipsk_news(category)[category])
        send_news_page(bot, call.message, news, page, _type=category)
    except Exception as e:
        bot.send_message(
            call.message.chat.id, 
            f"Error: {e}"
            )

def handle_pagination(
        call: tb.types.CallbackQuery, 
        news_categories: dict) -> None:
    """Handles pagination.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
        news_categories (dict): News categories.
    Returns: None
    """
    number_str = call.data.split('#')[0]
    if number_str=='number':
        call_data = call.data.split('#')[2]
        if call_data in news_categories['pln']:
            handle_pln_pagination(call)
        elif call_data in news_categories['cdi']:
            handle_cdi_pagination(call)
        elif call_data in news_categories['ipsk']:
            handle_ipsk_pagination(call)

def handle_news_categories(
        call: tb.types.CallbackQuery, 
        news_categories: dict) -> None:
    """Handles news categories.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
        news_categories (dict): News categories.
    Returns: None
    """
    if call.data in news_categories['pln']:
        handle_pln_callback_query(call)
    elif call.data in news_categories['cdi']:
        handle_cdi_callback_query(call)
    elif call.data in news_categories['ipsk']:
        handle_ipsk_callback_query(call)

@bot.message_handler(commands=["start"])
def handle_start(msg: tb.types.Message) -> None:
    """Handles start command.

    Args:
        msg (tb.types.Message): Message instance.
    Returns: None
    """
    bot.send_message(
        chat_id=msg.chat.id,
        text=f"""
Hi, {msg.from_user.first_name}
Here you can get the latest regional news
        """,
        parse_mode='MarkdownV2',
        reply_markup=kb.get_main_inline_markup()
    )
    db.insert_data(
        conn, 
        cursor, 
        'settings', 
        (msg.from_user.id, 'pagination_off'))

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call: tb.types.CallbackQuery) -> None:
        """Handles callback query.

    Args:
        call (tb.types.CallbackQuery): Callback query instance.
    Returns: None
    """
        news = {
            'pln': ['today', 'accidents', 'automir', 'culture', 'society'],
            'cdi': ['news', 'rbusiness', 'rmarket', 'rrabota'],
            'ipsk': ['allnews']
        }
        delete_past_messages(bot, call, 100)
        handle_settings(bot, call)
        handle_pagination(call, news)
        handle_news_categories(call, news)
        handle_main_callback_query(bot, call)

bot.polling(none_stop=True)
