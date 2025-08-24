from flask import Flask, render_template
import requests
import psutil
from datetime import datetime, timedelta
import os
from flask_basicauth import BasicAuth
import platform
import requests
from flask import request, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/projects')
def projects_page():
    return render_template('projects.html')

@app.route('/education')
def education_page():
    return render_template('education.html')

@app.route('/experience')
def experience_page():
    return render_template('work_history.html')


app.config['BASIC_AUTH_USERNAME'] = 'changeme'
app.config['BASIC_AUTH_PASSWORD'] = 'changeme'
basic_auth = BasicAuth(app)

@app.route("/admin-stats")
@basic_auth.required
def admin_stats():
    # System uptime
    uptime_seconds = (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
    uptime = str(timedelta(seconds=int(uptime_seconds)))

    # Public IP
    try:
        public_ip = requests.get('https://api64.ipify.org').text
    except requests.RequestException:
        public_ip = "Unable to fetch public IP"

    # Network interfaces and traffic
    network_stats = psutil.net_io_counters()
    network_info = {
        "bytes_sent": network_stats.bytes_sent // (1024 * 1024),
        "bytes_recv": network_stats.bytes_recv // (1024 * 1024),
        "packets_sent": network_stats.packets_sent,
        "packets_recv": network_stats.packets_recv,
    }

    # Pass minimal stats to the template
    stats = {
        "uptime": uptime,
        "public_ip": public_ip,
        "network": network_info,
    }

    return render_template("admin_stats.html", stats=stats)


## capcha part
RECAPTCHA_SECRET_KEY = "changeme"

@app.route("/validate-captcha", methods=["POST"])
def validate_captcha():
    token = request.json.get("token")
    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    })
    result = resp.json()
    return jsonify({"success": result.get("success", False)})



if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    #print(f"Running on http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000)#,debug=True)



