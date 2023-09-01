import logging
from typing import List, Dict

from aiohttp import ClientSession

from src.database import redis_db


class APIParser:
    CARD_INFO_URL: str = 'https://card.wb.ru/cards/detail?appType=1&spp=0&nm='
    FEEDBACKS_URL: str = 'https://feedbacks2.wb.ru/feedbacks/v1/'

    async def parse(self) -> Dict:
        """ Parse site and get new feedbacks """
        sku_list = await redis_db.get_all()
        logging.info('SKU received.')
        data = await self.__get_data_for_notification(sku_list)
        logging.info('New feedbacks received.')
        await self.__update_feedback_id(data)
        logging.info('Redis data updated successfully.')

        return data

    async def __get_data_for_notification(self, sku_list: List[int]) -> Dict:
        for_notification = {}
        for sku in sku_list:
            async with ClientSession() as session:
                root_list = await self.__get_root(session, category_id=sku)
                new_feedbacks = await self.__collect_feedback(session, root_list=root_list)
                if new_feedbacks:
                    for_notification.update(new_feedbacks)

        return for_notification

    async def __get_root(self, session: ClientSession, category_id: int) -> List[Dict]:
        root = []
        url = f'{self.CARD_INFO_URL}{category_id}'
        async with session.get(url=url) as response:
            if response.status != 200:
                logging.error(f'[API REQUEST ERROR] STATUS [{response.status}] REASON: [{response.reason}]')
                return root

            data = await response.json()
            products = data.get('data').get('products')
            for value in products:
                root_value = value.get('root')
                if root_value not in root:
                    root.append(
                        {
                            'root': root_value,
                            'sku': category_id,
                            'name': value.get('name')
                        }
                    )

        return root

    async def __collect_feedback(self, session: ClientSession, root_list: List[Dict]) -> Dict:
        result = {}
        for value in root_list:
            root_id = value.get('root')
            sku = value.get('sku')
            if sku not in result:
                result[sku] = {}

            url = f'{self.FEEDBACKS_URL}{root_id}'
            async with session.get(url=url) as response:
                if response.status != 200:
                    logging.error(f'[API REQUEST ERROR] STATUS [{response.status}] REASON: [{response.reason}]')
                    continue

                data = await response.json()
                feedbacks = data.get('feedbacks')
                if feedbacks is not None:
                    redis_data = await redis_db.get_data(sku)
                    valuation = data.get('valuation')
                    old_feedbacks = redis_data.get('feedbacks_id') if redis_data is not None else []
                    new_feedbacks = self.__inspect(feedbacks, old_feedbacks)
                    if new_feedbacks:
                        result[sku] = {
                            'name': value.get('name'),
                            'valuation': valuation,
                            'new_feedbacks': new_feedbacks
                        }

        return result

    @staticmethod
    def __inspect(feedbacks: List[Dict], old_feedbacks: List[int]) -> List[Dict]:
        new_feedbacks = []
        for feedback in feedbacks:
            grade = feedback.get('productValuation')
            if grade < 5:
                id_ = feedback.get('id')
                if id_ not in old_feedbacks:
                    text = feedback.get('text')
                    new_feedbacks.append({
                        'id': id_,
                        'grade': grade,
                        'text': text
                    })

        return new_feedbacks

    @staticmethod
    async def __update_feedback_id(new_feedbacks: Dict):
        for sku in new_feedbacks:
            if new_feedbacks[sku]:
                id_ = [i.get('id') for i in new_feedbacks[sku]['new_feedbacks']]
                db_data = await redis_db.get_data(sku)
                current_feedbacks_id = db_data.get('feedbacks_id')
                current_feedbacks_id.extend(id_)
                await redis_db.update_data(
                    sku=sku,
                    feedbacks_id=current_feedbacks_id
                )


parser = APIParser()
