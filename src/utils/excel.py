from typing import List

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from .file_manager import file_manager


class Excel:
    def parse(self, file_path: str) -> List[int]:
        """
        Parse excel-file and collect SKU data.
        :param file_path: Path ot excel-file.
        :return:
        List of SKU
        """
        wb = self.__get_workbook(file_path)
        sku = self.__parse(wb)
        file_manager.remove_file(file_path)
        return sku

    @staticmethod
    def __get_workbook(file_path: str) -> Workbook:
        return load_workbook(file_path)

    @staticmethod
    def __parse(workbook: Workbook) -> List[int]:
        ws = workbook.active
        return [value[0] for value in ws.values]


excel = Excel()
