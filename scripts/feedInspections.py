import http.client, json, urllib

bToken = '3bafd37fcd1fa5c1bd6156c6342075b9e4c8240ea9c9d448c807b6ef0e0faf12'

def feedItems():
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {bToken}'
    }

    conn.request('GET', '/feed/inspection_items?archived=false&completed=true&modified_after=2024-01-25T15%3A57%3A38.809Z', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    nextPage = parsed.get('metadata', {}).get('next_page', '')
    items = parsed.get('data', [])

    while nextPage:
        conn = http.client.HTTPSConnection('api.safetyculture.io')

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {bToken}'
        }

        conn.request('GET', nextPage, headers=headers)

        res = conn.getresponse()
        raw = res.read().decode('utf-8')
        parsed = json.loads(raw)

        nextPage = parsed.get('metadata', {}).get('next_page', '')
        dataToAdd = parsed.get('data', [])
        items.extend(dataToAdd)

    siteRef = {}
    for row in items:
        if row['type'] == 'site':
            audit_id = row.get('audit_id', '')
            site = row.get('response', '')
            if site:
                siteRef[audit_id] = site

    for row in items:
        audit_id = row.get('audit_id', '')
        if audit_id in siteRef:
            row['site'] = siteRef[audit_id]

    return items

def feedInspections():
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {bToken}'
    }

    conn.request('GET', '/feed/inspections?archived=false&completed=true&modified_after=2024-01-25T15%3A57%3A38.809Z', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    nextPage = parsed.get('metadata', {}).get('next_page', '')
    inspections = parsed.get('data', [])

    while nextPage:
        conn = http.client.HTTPSConnection('api.safetyculture.io')

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {bToken}'
        }

        conn.request('GET', nextPage, headers=headers)

        res = conn.getresponse()
        raw = res.read().decode('utf-8')
        parsed = json.loads(raw)

        nextPage = parsed.get('metadata', {}).get('next_page', '')
        dataToAdd = parsed.get('data', [])
        inspections.extend(dataToAdd)

    return inspections

def marry():
    inspections = feedInspections()
    items = feedItems()[:1]

    completedRef = {row.get('id', ''): row.get('date_completed', '') for row in inspections}

    for row in items:
        audit_id = row['audit_id']
        if audit_id in completedRef:
            row['completed'] = completedRef[audit_id][:10]

    return items

marry()