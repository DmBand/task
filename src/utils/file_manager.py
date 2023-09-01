import os
from typing import Union

from aiogram.types import Message

from src.config import TMP_DIR, bot
from .messanger import messanger


class FileManager:
    async def download_file(self, message: Message) -> Union[str, None]:
        """
        Download user document.
        :return:
        Path to downloaded file
        """
        file_id = self.__get_file_id(message)
        if file_id is None:
            await message.answer(messanger.invalid_format)
        else:
            filename = self.__get_filename(message)
            path_to_file = await self.__download_file(file_id, filename)

            return path_to_file

    @staticmethod
    def remove_file(path: str) -> None:
        os.remove(path)

    @staticmethod
    def __get_file_id(message: Message) -> Union[str, None]:
        allowed_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
        mime_type = message.document.mime_type
        if mime_type in allowed_types:
            return message.document.file_id

        return None

    @staticmethod
    def __get_filename(message: Message) -> str:
        return message.document.file_name

    @staticmethod
    async def __download_file(file_id: str, filename: str) -> str:
        file = await bot.get_file(file_id)
        file_path = file.file_path
        save_to = os.path.join(TMP_DIR, filename)
        await bot.download_file(file_path, save_to)

        return save_to


file_manager = FileManager()
