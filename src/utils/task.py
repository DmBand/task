import logging

from . import notificator
from . import parser


async def schedule_task():
    logging.info('Parsing started.')
    data = await parser.parse()
    await notificator.send_feedbacks(data)
    logging.info('Parsing finished.')
