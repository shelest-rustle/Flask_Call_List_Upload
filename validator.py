import os

from dotenv import load_dotenv

from config import *

load_dotenv()


def check_content_type_json(request):
    if request.headers.get('Content-Type') != 'application/json':
        return {"error": "Content-Type must be application/json"}


def check_required(key, value):
    if not value or value == "":
        return {"error": f"{key} can not be empty"}


def check_string(param):
    if not isinstance(param, str):
        return {"error": f"{param} must be string"}


def check_sum(sum: str):
    if not sum.isdigit():
        if "," not in sum:
            return {"error": "sum separator must be comma : ','"}


def check_due_date(due_date: str):
    if due_date:
        if not due_date.isdigit():
            return {"error": f"due_date value must be digit (str)\nvalue:{due_date}, type:{type(due_date)}"}


def is_valid_client(client: dict, agent: str):
    required_data = INITIALS
    if agent == "agent_example_special":
        required_data += ["sum_field_3", ]
    required_values = os.environ.get("REQUIRED_VALUES_INITIALS")
    for key in required_data:
        if key not in client:
            if key == "phone":
                return {"error": f"{key} is not provided for {client['CID']}"}
            message = f"{key} is not provided for {client['phone']}"
            if key not in required_values:
                message += f". If no {key}, should be empty"
            return {"error": message}
        if key in required_values:
            is_empty = check_required(key, client[key])
            if is_empty:
                if client["phone"]:
                    is_empty["phone"] = client["phone"]
                else:
                    is_empty["CID"] = client["CID"]
                return is_empty
        is_not_string = check_string(client[key])
        if is_not_string:
            return is_not_string
        if key == "sum_field_1":
            is_incorrect_sum_field_1 = check_sum(client[key])
            if is_incorrect_sum_field_1:
                is_incorrect_sum_field_1["phone"] = client["phone"]
                return is_incorrect_sum_field_1
        if key == "sum_field_2":
            if client[key]:
                is_incorrect_sum_field_2 = check_sum(client[key])
                if is_incorrect_sum_field_2:
                    is_incorrect_sum_field_2["phone"] = client["phone"]
                    return is_incorrect_sum_field_2
        if agent == "agent_example_special":
            if key == "sum_field_3":
                if client[key]:
                    is_incorrect_ins = check_sum(client[key])
                    if is_incorrect_ins:
                        is_incorrect_ins["phone"] = client["phone"]
                        return is_incorrect_ins
        if key == "due_date":
            is_incorrect_due_date = check_due_date(client[key])
            if is_incorrect_due_date:
                return is_incorrect_due_date
    return True


def is_valid_json(json: dict):
    required_data = os.environ.get("JSON_REQUIRED_DATA")
    for key in required_data:
        if key not in json:
            return {"error": f"{key} is not provided"}
        if key == "agent":
            if json[key] not in AGENTS:
                return {"error": f"Incorrect agent {json["agent"]}, acceptable values: {AGENTS}"}
        if key == "data":
            if len(json[key]) == 0:
                return {"error": "data can not be empty"}
            for client in json[key]:
                client_check = is_valid_client(client, json["agent"])
                if not isinstance(client, bool):
                    return client_check
    return True
