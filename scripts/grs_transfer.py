import http.client, json, urllib

origin_token = 'd59b7d50558b7539fc8d6ecaa9a2a213a5843987c4d240eb127b0ef0a2dcf158'
destination_token = '3bafd37fcd1fa5c1bd6156c6342075b9e4c8240ea9c9d448c807b6ef0e0faf12'

def listAllGrs():
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {origin_token}'
    }

    conn.request('GET', '/response_sets/v2', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    rawGrs = parsed.get('response_sets', [])

    allGrs = [grs['responseset_id'] for grs in rawGrs]

    return allGrs


def getGrs(grsId):
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {origin_token}'
    }

    conn.request('GET', f'/response_sets/{grsId}', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    resRaw = parsed.get('responses')
    responses = [{'label': grs['label'], 'short_label': grs['label'][:19]} for grs in resRaw]
    name = parsed.get('name')

    return responses, name


def createGrs(responses, name):
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {destination_token}'
    }

    payload = {
        'name': name, 
        'responses': responses
    }

    Spayload = json.dumps(payload)

    conn.request('POST', '/response_sets', Spayload, headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    newGrsId = parsed.get('responseset_id')
    newGrsName = parsed.get('name')

    print(newGrsId, newGrsName)

    return newGrsId, newGrsName


def processTransfer():
    allGrs = listAllGrs()

    for grs in allGrs:
        rs = getGrs(grs)
        responses = rs[0]
        name = rs[1]
        createGrs(responses, name)


processTransfer()