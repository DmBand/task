import asyncio
import logging
from typing import Dict, Union

from src.config import bot, CHAT_ID


class Notificator:
    async def send_feedbacks(self, data: Dict) -> None:
        """ Send feedbacks to the telegram chat """
        logging.info('Notifications started.')
        await self.__send_feedbacks(data)
        logging.info('Notifications finished.')

    async def __send_feedbacks(self, data: Dict) -> None:
        for sku in data:
            if data[sku]:
                valuation = data[sku]['valuation']
                name = data[sku]['name']
                new_feedbacks = data[sku]['new_feedbacks']
                for feedback in new_feedbacks:
                    message = self.__create_message(
                        sku=sku,
                        name=name,
                        grade=feedback.get('grade'),
                        text=feedback.get('text'),
                        valuation=valuation
                    )

                    await self.__send(message)

    @staticmethod
    def __create_message(sku: Union[str, int], name: str, grade: int, text: str, valuation: Union[int, float]) -> str:
        message = '<b>НОВЫЙ НЕГАТИВНЫЙ ОТЗЫВ</b>\n\n'
        message += (f'<b>SKU</b>: {sku}\n\n'
                    f'<b>Товар</b>: {name}\n\n'
                    f'<b>Оценка</b>: {grade}\n\n'
                    f'<b>Текст</b>: {text}\n\n'
                    f'<b>Рейтинг товара</b>: {valuation}')

        return message

    @staticmethod
    async def __send(message: str) -> None:
        await bot.send_message(text=message, chat_id=CHAT_ID)
        await asyncio.sleep(3)


notificator = Notificator()
