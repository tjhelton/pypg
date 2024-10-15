from datetime import datetime, timedelta

pSunday = (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d')
today = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

print(today, pSunday)
