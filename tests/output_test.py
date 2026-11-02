from modules.output import JsonOutput, CsvOutput
import json, csv

def test_json_output(report, tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)
    path = tmp_path / 'crypto_report.json'

    json_output = JsonOutput(report)
    json_output.output()

    assert path.exists()

    with open(path, 'r', encoding= 'UTF-8' ) as jf:
        data = json.load(jf)

        assert data == report.__dict__


def test_csv_output(report, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / 'crypto_report.csv'
    csv_output = CsvOutput(report)
    csv_output.output()

    assert path.exists()
    with open(path, 'r', encoding='UTF-8') as cf:
        reader = csv.DictReader(cf)
        rows = list(reader)
        expected_row = {
                'type': 'gainer',
                'rank': '1',
                'name': report.top_gainers[0]['name'],
                'symbol': report.top_gainers[0]['symbol'],
                'change_24h': str(report.top_gainers[0]['change_24h'])
            }

        expected_fieldnames = ['type', 'rank', 'name', 'symbol', 'change_24h']

        assert reader.fieldnames == expected_fieldnames
        assert len(report.top_gainers) + len(report.top_losers) == len(rows)
        assert rows[0] == expected_row

        expected_row_losers = {
                'type': 'loser',
                'rank': '1',
                'name': report.top_losers[0]['name'],
                'symbol': report.top_losers[0]['symbol'],
                'change_24h': str(report.top_losers[0]['change_24h'])
            }

        loser_index = len(report.top_gainers)
        assert rows[loser_index] == expected_row_losers