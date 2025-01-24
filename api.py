import json

from requests.auth import HTTPBasicAuth

from config import *


def take_token():
    headers = {}
    data = {}
    try:
        response = requests.post(
            URL_AUTH,
            auth=HTTPBasicAuth(API_LOGIN, API_PASSWORD),
            data=data,
            headers=headers
        )
        data = response.json()
        token = data['token']
        LOGGER.info('Получили токен успешно')
        return token
    except Exception as take_token_error:
        raise Exception(take_token_error)


def send_data(call_list, agent_name, selection_name):
    LOGGER.info('Попали в send_data')
    try:
        params = {
            'agent_uuid': UUIDS[agent_name],
            'with_selection': 'true',
            'selection_name': f"{selection_name}"
        }

        payload = json.dumps(call_list)
        headers = {
            "Authorization": f"Bearer {take_token()}",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", URL_QUEUE_LOADER, headers=headers, data=payload, params=params)
        status_code = response.status_code
        LOGGER.info(f'Ответ send_data: {response.json()}')
        return status_code
    except Exception as err:
        msg = f"Ошибка загрузки данных на агента {agent_name}: {err}"
        LOGGER.info(msg)
        send_tg(msg)
