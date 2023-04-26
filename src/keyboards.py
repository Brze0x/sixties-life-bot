import telebot as tb
from pagination import InlineKeyboardPaginator


# Create an inline keyboard for main menu
def get_main_inline_markup():
    inline_keyboard =  tb.types.InlineKeyboardMarkup()
    inline_keyboard.add(
        tb.types.InlineKeyboardButton('PLN', callback_data='pln'),
        tb.types.InlineKeyboardButton('CDI', callback_data='cdi'),
        tb.types.InlineKeyboardButton('IPSK', callback_data='ipsk')
    ).row(
        tb.types.InlineKeyboardButton('Settings', callback_data='settings'),
    )
    return inline_keyboard

# Create an inline keyboard for settings menu
def get_settings_inline_markup():
    inline_keyboard =  tb.types.InlineKeyboardMarkup()
    inline_keyboard.add(
        tb.types.InlineKeyboardButton('Pagination Off', callback_data='pagination_off'),
        tb.types.InlineKeyboardButton('Pagination On', callback_data='pagination_on'),
    ).row(
        tb.types.InlineKeyboardButton('Back', callback_data='back')
    )
    return inline_keyboard

# Create an inline keyboard for PLN news
def get_pln_inline_markup():
    inline_keyboard =  tb.types.InlineKeyboardMarkup()
    inline_keyboard.add(
        tb.types.InlineKeyboardButton('Today', callback_data='today'),
        tb.types.InlineKeyboardButton('Accidents', callback_data='accidents'),
        tb.types.InlineKeyboardButton('Automir', callback_data='automir'),
        tb.types.InlineKeyboardButton('Culture', callback_data='culture'),
        tb.types.InlineKeyboardButton('Society', callback_data='society'),
        row_width=3
    ).row(
        tb.types.InlineKeyboardButton('Back', callback_data='back')
    )
    return inline_keyboard

# Create an inline keyboard for CDI news
def get_cdi_inline_markup():
    inline_keyboard =  tb.types.InlineKeyboardMarkup()
    inline_keyboard.add(
        tb.types.InlineKeyboardButton('CDI News', callback_data='news'),
        tb.types.InlineKeyboardButton('Market', callback_data='rmarket'),
        tb.types.InlineKeyboardButton('Business', callback_data='rbusiness'),
        tb.types.InlineKeyboardButton('Rabota', callback_data='rrabota'),
        row_width=2
    ).row(
        tb.types.InlineKeyboardButton('Back', callback_data='back')
    )
    return inline_keyboard

# Create an inline keyboard for IPSK news
def get_ipsk_inline_markup():
    inline_keyboard =  tb.types.InlineKeyboardMarkup()
    inline_keyboard.add(
        tb.types.InlineKeyboardButton('IPSK News', callback_data='allnews'),
        row_width=1
    ).row(
        tb.types.InlineKeyboardButton('Back', callback_data='back')
    )
    return inline_keyboard

def get_pagination_inline_markup():
    inline_keyboard =  tb.types.InlineKeyboardMarkup()
    inline_keyboard.add(
        tb.types.InlineKeyboardButton('Prev', callback_data='prev'),
        tb.types.InlineKeyboardButton('Next', callback_data='next')
    ).row(
        tb.types.InlineKeyboardButton('Back', callback_data='back')
    )
    return inline_keyboard

class Pagination(InlineKeyboardPaginator):
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'