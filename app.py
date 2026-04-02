from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import uuid
import ecpay_utils
import email_utils

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return app.send_static_file('index.html')

@app.route('/assets/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('assets/images', filename)

@app.route('/success', methods=['GET', 'POST'])
def success():
    return app.send_static_file('success.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    email = request.form.get('email')
    order_id = "VCD" + uuid.uuid4().hex[:17].upper()
    amount = 299
    host = os.environ.get('APP_DOMAIN', "http://127.0.0.1:5000")
    html_form = ecpay_utils.build_ecpay_form(
        order_id=order_id,
        amount=amount,
        return_url=f"{host}/api/ecpay/return",
        client_back_url=f"{host}/success",
        buyer_email=email
    )
    return render_template_string(html_form)

@app.route('/api/ecpay/return', methods=['POST'])
def ecpay_return():
    data = request.form.to_dict()
    if ecpay_utils.verify_mac_value(data) and data.get('RtnCode') == '1':
        buyer_email = data.get('CustomField1')
        if buyer_email:
            print(f"DEBUG_TRIGGER_EMAIL: {buyer_email}"); email_utils.send_download_email(buyer_email)
    return '1|OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
