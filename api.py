from flask import Flask, request, send_file, jsonify, render_template
from pickle import dump, load

dbread = open('stats.picklejar', 'rb')

app = Flask(__name__)

browsers = load(dbread)

def find_btype(item):
    return len(list(filter(lambda browseritem: browseritem['type'] == item, browsers)))

def return_num_browsers():
    chrome = find_btype('Chrome')
    if chrome is None:
        chrome = 0
    firefox = find_btype('Firefox')
    if firefox is None:
        firefox = 0
    edge = find_btype('Edge')
    if edge is None:
        edge = 0
    ie = find_btype('IE')
    if ie is None:
        ie = 0
    safari = find_btype('Safari')
    if safari is None:
        safari = 0
    other = len(browsers) - chrome - firefox - edge - ie - safari
    if other is None:
        other = 0
    return [chrome, firefox, edge, ie, safari, other]

def write_to_file():
    dbwrite = open('stats.picklejar', 'wb')
    dump(browsers, dbwrite)

@app.route('/pywebanalytics.js')
def serve_js():
    return send_file('pywebanalytics.js')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html', browserData=return_num_browsers())

@app.route('/demo')
def demo():
    print(browsers)
    return '<script src="/pywebanalytics.js"></script><p style="font-family: Calibri, sans-serif">This is a demo page with analytics.</p>'

@app.route("/endpoint", methods=['POST'])
def endpoint():
    browser = {}
    browser['type'] = request.json['browser']['name']
    browser['version'] = request.json['browser']['version']
    browsers.append(browser)
    write_to_file()
    return jsonify(browser)

app.run(port=80, debug=False)