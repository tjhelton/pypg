import http.client
import json

ORIGIN = 'TOKEN'
DESTINATION = 'TOKEN'

def list_all_grs():
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {ORIGIN}'
    }

    conn.request('GET', '/response_sets/v2', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    raw_grs = parsed.get('response_sets', [])

    all_grs = [grs['responseset_id'] for grs in raw_grs]

    return all_grs

def get_grs(grs_id):
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {ORIGIN}'
    }

    conn.request('GET', f'/response_sets/{grs_id}', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    res_raw = parsed.get('responses')
    responses = [{'label': grs['label'], 'short_label': grs['label'][:19]} for grs in res_raw]
    name = parsed.get('name')

    return responses, name

def create_grs(responses, name):
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {DESTINATION}'
    }

    payload = {
        'name': name, 
        'responses': responses
    }

    s_payload = json.dumps(payload)

    conn.request('POST', '/response_sets', s_payload, headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    new_grs_id = parsed.get('responseset_id')
    new_grs_name = parsed.get('name')

    return new_grs_id, new_grs_name

def process_transfer():
    all_grs = list_all_grs()

    for grs in all_grs:
        rs = get_grs(grs)
        responses = rs[0]
        name = rs[1]
        create_grs(responses, name)

process_transfer()
