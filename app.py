import requests
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def get_player_info(account_uid, datadome="HfMB_IAV7n1ukAwspLFKxECKCRG29zGP1MIHyEet5_uPyo2hyIfNOwUkUseVibwwpLamoRBFB6ZldreSo_0qa5Piv3f~qJd_0n0PrR8oZWGCaNafifAyAAMIh1KRfbzc"):
    if not account_uid:
        return {'error': 'error account_uid'}

    url = 'https://napthe.vn/api/auth/player_id_login'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "x-datadome-clientid": datadome,
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://napthe.vn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://napthe.vn/app/100067/idlogin",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cookie": "source=mb; mspid2=1a8665f2a24f5f5e310f181cca289f15"
    }

    payload = {
        "app_id": 100067,
        "login_id": account_uid,
        "app_server_id": 0,
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }

    try:
        logging.debug(f"Sending request with account_uid: {account_uid}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        if 'error' in response_data:
            logging.error(f"Error in response: {response_data['error']}")
            return {'error': response_data['error']}

        region = response_data.get('region', 'error')
        nickname = response_data.get('nickname', 'error')
        nickname = ''.join(c for c in nickname if c not in '<>')

        return {
            'region': region,
            'nickname': nickname
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
        return {'error': str(e)}

@app.route('/api/region', methods=['GET'])
def region():
    account_uid = request.args.get('uid')
    if not account_uid:
        return jsonify({'error': 'uid is required'}), 400

    result = get_player_info(account_uid)
    if 'error' in result:
        return jsonify(result), 400

    result['credit'] = '@scromnyi_modz'
    return jsonify(result)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Free Fire API!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
