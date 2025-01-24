import json
import pandas
import datetime

from api import send_data
from config import *


class Refactor:

    def __init__(self, data, agent_name: str):
        self.origin_df = pandas.DataFrame(data)
        print(self.origin_df)
        self.result_df = pandas.DataFrame()
        self.call_list = []
        self.empty_due_date = 0
        self.agent_name = agent_name
        now = datetime.datetime.now()
        self.load_date = datetime.datetime.strftime(now, "%d_%m")

    def load_data(self):
        LOGGER.info("load_data func")
        upload_status = send_data(self.call_list, self.agent_name, f"API_{self.agent_name}_{self.load_date}")
        if str(upload_status) not in ('200', '202'):
            send_tg(f'Агент {self.agent_name}: загрузка очереди не удалась, статус: {upload_status}')
        else:
            send_tg(f'Агент {self.agent_name} успешно загружен по API\nКоличество контактов: {len(self.call_list)}', type_msg="info")
        return upload_status

    def clear_due_date(self):
        LOGGER.info("clear_due_date func")
        self.empty_due_date = self.origin_df["due_date"].isna().sum()
        LOGGER.info(f"Загружено пустого due_date: {self.empty_due_date}")
        self.origin_df = self.origin_df.dropna(subset=['due_date'])

    def change_column_types(self):
        self.result_df = self.result_df.fillna('')
        for column in self.result_df:
            self.result_df[column] = self.result_df[column].astype(str)

    def make_call_list(self):
        LOGGER.info("make_call_list func")
        result = json.loads(self.result_df.to_json(orient='index'))
        self.call_list = [result[r] for r in result]

    def __str__(self):
        return str(type(self).__name__)

    def plus_sums(self):
        LOGGER.info("plus_delay_and_commission func")
        """ Складывает столбцы sum_field_example_1 & sum_field_example_2 & sum_field_example_3 """
        self.origin_df['sum_field_example_1'] = self.origin_df['sum_field_example_1'].apply(lambda x: int(x) if x.isdigit() else float(x.replace(",", ".")))
        try:
            self.origin_df['sum_field_example_2'] = self.origin_df['sum_field_example_2'].apply(lambda x: int(x) if x and x.isdigit() else float(x.replace(",", ".")))
        except:
            LOGGER.info("отсутствует sum_field_example_2")
            self.origin_df['sum_field_example_2'] = 0
        self.origin_df['sum_field_example_1'] = self.origin_df[['sum_field_example_1', 'sum_field_example_2']].sum(axis=1)
        if 'sum_field_example_3' in self.origin_df.columns:
            try:
                self.origin_df['sum_field_example_3'] = self.origin_df['sum_field_example_3'].apply(lambda x: int(x) if x and x.isdigit() else float(x.replace(",", ".")))
            except:
                LOGGER.info("отсутствует sum_field_example_3")
                self.origin_df['sum_field_example_3'] = 0
            self.origin_df['sum_field_example_1'] = self.origin_df[['sum_field_example_1', 'sum_field_example_3']].sum(axis=1)

    def drop_another_sums(self):
        LOGGER.info("drop_another_sums func")
        if 'sum_field_example_2' in self.origin_df.columns:
            self.origin_df.drop('sum_field_example_2', axis=1, inplace=True)
        if 'sum_field_example_3' in self.origin_df.columns:
            self.origin_df.drop('sum_field_example_3', axis=1, inplace=True)

    def make_result_df(self):
        LOGGER.info("make_result_df func")
        self.result_df["phone"] = self.origin_df["phone"].astype(str).str[-10:]
        self.result_df["fio"] = self.origin_df["fio"]
        self.result_df["sum_field_1"] = self.origin_df["sum_field_1"]
        self.result_df["due_date"] = self.origin_df["due_date"]
        self.result_df["custom_field_1"] = self.origin_df["custom_field_1"]
        self.result_df["custom_field_2"] = ""

    def make_refactoring_and_write_json(self):
        LOGGER.info("make_refactoring_and_write_json func")
        self.clear_due_date()
        self.plus_sums()
        self.drop_another_sums()
        self.make_result_df()
        self.change_column_types()
        self.make_call_list()
