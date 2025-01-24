import json
import os
import datetime

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from flask_cors import CORS
from dotenv import load_dotenv

from validator import is_valid_json, check_content_type_json
from config import *
from tools import Refactor

load_dotenv()

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get("BASIC_AUTH_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("BASIC_AUTH_PASSWORD")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

basic_auth = BasicAuth(app)

@app.route('/bulk_upload', methods=['POST'])
@basic_auth.required
def bulk_upload():
    request_time = datetime.datetime.now() + datetime.timedelta(hours=5)
    LOGGER.info(f"/bulk_upload requested: {request_time}")
    LOGGER.info("validation start")
    check_content_type = check_content_type_json(request)
    LOGGER.info(f"check_content_type: {check_content_type}")
    if check_content_type:
        return jsonify(check_content_type), 400
    LOGGER.info("content_type OK")
    data = request.json
    data_validation = is_valid_json(data)
    LOGGER.info(f"data_validation: {data_validation}")
    if not isinstance(data_validation, bool):
        send_tg(f"/bulk_upload {request_time} validation error: {data_validation}")
        return jsonify(data_validation), 400
    LOGGER.info("data OK")
    upload = Refactor(data=data["data"], agent_name=data["agent"])
    LOGGER.info(f"refactor created for {data['agent']}")
    upload.make_refactoring_and_write_json()
    upload_status = upload.load_data()
    return jsonify({"upload_status": upload_status}), upload_status


@app.route('/send_results', methods=['POST'])
def send_results():
    LOGGER.info(f"/send_results requested: {datetime.datetime.now() + datetime.timedelta(hours=5)}")
    try:
        data = request.json
        LOGGER.info(f"data: {data}")
        url = os.environ.get("URL_SEND_RESULTS")
        payload = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        LOGGER.info(f"response code: {response.status_code}")
        if response.status_code not in (200, 201, 202):
            send_tg(f"ошибка отправки результатов: {response.text}")
            return jsonify({"error": response.json()}), response.status_code
        return jsonify({"send_results_status": response.status_code}), response.status_code
    except Exception as err:
        LOGGER.info(f"Ошибка send_results: {err}")
        return jsonify({"error": err}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
