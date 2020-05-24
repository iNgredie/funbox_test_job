from flask import Flask, request, jsonify
import redis
import time
from tldextract import extract


app = Flask(__name__)
r = redis.Redis()
timer = int(round(time.time()))


def get_domain(url):
    subdomain, domain, suffix = extract(url)
    return domain + '.' + suffix


@app.route('/visited_links', methods=['POST'])
def visited_links():
    content = request.get_json()
    links = content['links']
    for link in links:
        r.sadd(timer, link)
    return jsonify({'status': 'OK'})


@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    start = int(request.args.get('from', ''))
    stop = int(request.args.get('to', ''))
    domains_list, unique_domains = [], []
    output = {}
    for elem in range(start, stop + 1):
        if r.smembers(elem) != set():
            for item in r.smembers(elem):
                domains_list.append(str(item)[2:-1])
    for domain in domains_list:
        gt = get_domain(domain)
        if gt not in unique_domains:
            unique_domains.append(gt)
    output['domains'] = unique_domains
    output["status"] = "OK"
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)




