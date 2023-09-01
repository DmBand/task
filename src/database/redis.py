import json
from typing import List, Dict, Union

from redis import asyncio as aioredis
from redis.asyncio.client import Redis

from src.config import REDIS_MAIN_DB_URL


class RedisManager:

    async def set_new_sku(self, sku_list: List[Union[int, str]]) -> None:
        """ Set new sku data """
        conn = await self.__get_connection()
        for sku in sku_list:
            if not await conn.get(sku):
                data = json.dumps({'feedbacks_id': []})
                await conn.set(sku, data)
        await self.__close_connection(conn)

    async def get_all(self) -> List[str]:
        """ Get all SKU """
        conn = await self.__get_connection()
        keys = await conn.keys()

        return keys

    async def get_data(self, sku: Union[int, str]) -> Dict:
        """ Get feedbacks id for a specific SKU """
        conn = await self.__get_connection()
        string = await conn.get(sku)
        data = json.loads(string)
        await self.__close_connection(conn)

        return data

    async def update_data(self, sku: Union[int, str], feedbacks_id: List[str]) -> None:
        """ Update SKU data """
        conn = await self.__get_connection()
        data = json.dumps({'feedbacks_id': feedbacks_id})
        await conn.set(sku, data)
        await self.__close_connection(conn)

    async def remove_data(self, sku: Union[int, str]) -> None:
        """ Remove SKU data """
        conn = await self.__get_connection()
        await conn.delete(sku)
        await self.__close_connection(conn)

    @staticmethod
    async def __get_connection() -> Redis:
        return aioredis.from_url(REDIS_MAIN_DB_URL, decode_responses=True)

    @staticmethod
    async def __close_connection(conn: Redis) -> None:
        await conn.close()


redis_db = RedisManager()
