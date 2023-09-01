from aiogram import types


class Keyboard:
    def main_menu(self) -> types.ReplyKeyboardMarkup:
        """ Main menu keyboard """
        keypad = self.__base_keypad()
        keypad.add('Добавить новые SKU', 'Удалить SKU')

        return keypad

    def back(self) -> types.ReplyKeyboardMarkup:
        """ Back keyboard """
        keypad = self.__base_keypad()
        keypad.add('Назад')

        return keypad

    @staticmethod
    def __base_keypad(width: int = 1) -> types.ReplyKeyboardMarkup:
        keypad = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=width
        )
        return keypad


keyboard = Keyboard()
