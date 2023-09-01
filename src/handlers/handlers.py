from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from src.database import redis_db
from src.utils import excel, file_manager, keyboard, messanger
from src.utils.states import MainState


async def start(message: types.Message):
    await message.answer(messanger.greeting)
    await message.answer(messanger.info, reply_markup=keyboard.main_menu())


async def new_data(message: types.Message):
    await MainState.add_data.set()
    await message.answer(messanger.add_sku, reply_markup=keyboard.back())


async def add_new_parse_data(message: types.Message, state: FSMContext):
    file_path = await file_manager.download_file(message)
    if file_path:
        sku = excel.parse(file_path)
        await redis_db.set_new_sku(sku)

    await state.finish()
    await message.answer(messanger.ok, reply_markup=keyboard.main_menu())


async def remove_data(message: types.Message):
    await MainState.remove_data.set()
    await message.answer(messanger.remove, reply_markup=keyboard.back())


async def remove(message: types.Message, state: FSMContext):
    sku = message.text
    await redis_db.remove_data(sku)
    await state.finish()
    await message.answer(messanger.success, reply_markup=keyboard.main_menu())


async def back(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=messanger.info, reply_markup=keyboard.main_menu())


async def get_info(message: types.Message):
    await message.answer(f'ID текущего чата: <code>{message.chat.id}</code>')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start,
        commands=['start']
    )
    dp.register_message_handler(
        new_data,
        Text(equals=['Добавить новые SKU']),
    )
    dp.register_message_handler(
        add_new_parse_data,
        content_types=types.ContentType.DOCUMENT,
        state=MainState.add_data
    )
    dp.register_message_handler(
        get_info,
        commands=['id']
    )
    dp.register_message_handler(
        remove_data,
        Text(equals=['Удалить SKU']),
    )
    dp.register_message_handler(
        remove,
        state=MainState.remove_data
    )
    dp.register_message_handler(
        back,
        Text(equals=['Назад', 'назад']),
        state=MainState.add_data
    )
    dp.register_message_handler(
        back,
        Text(equals=['Назад', 'назад']),
        state=MainState.remove_data
    )
