import csv

SAMPLE_DOC = 'Ontivity User Provisioning.csv'

def main():
    with open(SAMPLE_DOC, newline='') as file:
        raw = csv.DictReader(file)
        array = [{'title': row.get('positionTitle'), 'group': row.get('group')} for row in raw]
    print(array[:5])
    return

main()
