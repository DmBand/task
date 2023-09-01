from src.config import NOTIFICATION_MINUTES


class Messanger:
    @property
    def greeting(self) -> str:
        return 'Добро пожаловать!'

    @property
    def info(self) -> str:
        return (f'Бот собирает отзывы о товарах каждые <b>{NOTIFICATION_MINUTES} минут</b>.\n'
                f'Выберите действие.')

    @property
    def add_sku(self) -> str:
        return f'Пришлите файл в формате <b>xslx</b>.'

    @property
    def invalid_format(self) -> str:
        return '<b>НЕВЕРНЫЙ ФОРМАТ!</b>\n' \
               'Пришлите файл в формате <b>xslx</b>.'

    @property
    def ok(self) -> str:
        return 'Новые данные для парсинга успешно добавлены.'

    @property
    def remove(self) -> str:
        return 'Введите SKU товара и он будет удален из базы парсинга.'

    @property
    def success(self) -> str:
        return 'Данные успешно удалены.'


messanger = Messanger()
