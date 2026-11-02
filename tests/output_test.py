from modules.output import JsonOutput, CsvOutput, ConsoleOutput
from rich.text import Text

import json, csv
import pytest

@pytest.mark.parametrize('output_class',
                            [
                                JsonOutput,
                                CsvOutput,
                                ConsoleOutput
                            ]
                            )
def test_interface_output(output_class,
                          report,
                          tmp_path,
                          monkeypatch):
    monkeypatch.chdir(tmp_path)
    outputter = output_class(report)
    outputter.output()


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


def test_console_output(capfd, report):
    console_output = ConsoleOutput(report)
    console_output.output()
    captured = capfd.readouterr()
    plain_output = Text.from_ansi(captured.out).plain
    assert 'Топ Роста и Падения' in plain_output
    assert f'{report.top_gainers[0]["name"]}' in plain_output
    assert f'{report.highest_volume["name"]}' in plain_output
    assert f'Капитал рынка: {report.total_market_cap_usd}' in plain_output