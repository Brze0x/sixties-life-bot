import json
from collections import namedtuple


InlineKeyboardButton = namedtuple('InlineKeyboardButton', ['text', 'callback_data'])


class InlineKeyboardPaginator:
    _keyboard_before = None
    _keyboard = None
    _keyboard_after = None

    previous_page_label = '‹'
    next_page_label = '›'
    current_page_label = '·{}·'

    def __init__(self, page_count, current_page=1, data_pattern='{page}'):
        self._keyboard_before = []
        self._keyboard_after = []

        if current_page is None or current_page < 1:
            current_page = 1
        current_page = min(current_page, page_count)
        self.current_page = current_page

        self.page_count = page_count

        self.data_pattern = data_pattern

    def __str__(self):
        if self._keyboard is None:
            self._build()
        return ' '.join([btn['text'] for btn in self._keyboard])

    def _build(self):
        keyboard_dict = {}
        
        keyboard_dict = self._build_middle_keyboard()

        keyboard_dict[self.current_page] = self.current_page_label.format(self.current_page)

        self._keyboard = self._to_button_array(keyboard_dict)

    def _build_middle_keyboard(self):
        keyboard_dict = {}
        if self.current_page > 1:
            keyboard_dict[self.current_page-1] = self.previous_page_label.format(self.current_page-1)

        keyboard_dict[self.current_page] = self.current_page

        if self.current_page < self.page_count:
            keyboard_dict[self.current_page+1] = self.next_page_label.format(self.current_page+1)
        return keyboard_dict

    def _to_button_array(self, keyboard_dict):
        keys = sorted(keyboard_dict.keys())
        keyboard = [
            InlineKeyboardButton(
                text=str(keyboard_dict[key]),
                callback_data=self.data_pattern.format(page=key),
            )
            for key in keys
        ]
        return _buttons_to_dict(keyboard)

    @property
    def keyboard(self):
        if self._keyboard is None:
            self._build()

        return self._keyboard

    @property
    def markup(self):
        """InlineKeyboardMarkup"""
        keyboards = []

        keyboards.extend(self._keyboard_before)
        keyboards.append(self.keyboard)
        keyboards.extend(self._keyboard_after)

        keyboards = list(filter(bool, keyboards))

        return json.dumps({'inline_keyboard': keyboards}) if keyboards else None



    def add_before(self, *inline_buttons):
        self._keyboard_before.append(_buttons_to_dict(inline_buttons))

    def add_after(self, *inline_buttons):
        self._keyboard_after.append(_buttons_to_dict(inline_buttons))


def _buttons_to_dict(buttons):
    return [
        {
            'text': button.text,
            'callback_data': button.callback_data,
        }
        for button in buttons
    ]