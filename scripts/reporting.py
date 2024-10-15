import http.client
import json

BTOKEN = 'TOKEN'

def feed_items():
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {BTOKEN}'
    }

    conn.request('GET', '/feed/inspection_items?archived=false&completed=true&modified_after=2024-01-25T15%3A57%3A38.809Z', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    next_page = parsed.get('metadata', {}).get('next_page', '')
    items = parsed.get('data', [])

    while next_page:
        conn = http.client.HTTPSConnection('api.safetyculture.io')

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {BTOKEN}'
        }

        conn.request('GET', next_page, headers=headers)

        res = conn.getresponse()
        raw = res.read().decode('utf-8')
        parsed = json.loads(raw)

        next_page = parsed.get('metadata', {}).get('next_page', '')
        data_to_add = parsed.get('data', [])
        items.extend(data_to_add)

    site_ref = {}
    for row in items:
        if row['type'] == 'site':
            audit_id = row.get('audit_id', '')
            site = row.get('response', '')
            if site:
                site_ref[audit_id] = site

    for row in items:
        audit_id = row.get('audit_id', '')
        if audit_id in site_ref:
            row['site'] = site_ref[audit_id]

    return items

def feed_inspections():
    conn = http.client.HTTPSConnection('api.safetyculture.io')

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {BTOKEN}'
    }

    conn.request('GET', '/feed/inspections?archived=false&completed=true&modified_after=2024-01-25T15%3A57%3A38.809Z', headers=headers)

    res = conn.getresponse()
    raw = res.read().decode('utf-8')
    parsed = json.loads(raw)

    next_page = parsed.get('metadata', {}).get('next_page', '')
    inspections = parsed.get('data', [])

    while next_page:
        conn = http.client.HTTPSConnection('api.safetyculture.io')

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {BTOKEN}'
        }

        conn.request('GET', next_page, headers=headers)

        res = conn.getresponse()
        raw = res.read().decode('utf-8')
        parsed = json.loads(raw)

        next_page = parsed.get('metadata', {}).get('next_page', '')
        data_to_add = parsed.get('data', [])
        inspections.extend(data_to_add)

    return inspections

def marry():
    inspections = feed_inspections()
    items = feed_items()[:1]

    completed_ref = {row.get('id', ''): row.get('date_completed', '') for row in inspections}

    for row in items:
        audit_id = row['audit_id']
        if audit_id in completed_ref:
            row['completed'] = completed_ref[audit_id][:10]

    return items

marry()
