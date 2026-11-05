import csv
import json
import pytest
from rich.text import Text

import modules.output as output_module
from types import SimpleNamespace

from modules.output import (
    JsonOutput,
    CsvOutput,
    ConsoleOutput,
)

@pytest.mark.parametrize('output_class, expected',
                            [
                                (JsonOutput, 'crypto_report.json'),
                                (CsvOutput, 'crypto_report.csv'),
                                (ConsoleOutput, 'Топ Роста и Падения')
                            ]
                                )
def test_interface_output(output_class, expected,
                          report,
                          tmp_path,
                          monkeypatch,
                          capfd):
    monkeypatch.chdir(tmp_path)
    outputter = output_class(report)
    outputter.output()
    if output_class is ConsoleOutput:
        captured = capfd.readouterr()
        assert expected in captured.out
    else:
        path = tmp_path / expected
        assert path.exists()


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

        expected_fieldnames = [
            'type', 'rank', 'name', 'symbol', 'change_24h'
        ]

        expected_rows = []

        for i, coin in enumerate(report.top_gainers, start=1):
            expected_rows.append({
                'type': 'gainer',
                'rank': str(i),
                'name': coin['name'],
                'symbol': coin['symbol'],
                'change_24h': str(coin['change_24h'])
            })

        for i, coin in enumerate(report.top_losers, start=1):
            expected_rows.append({
                'type': 'loser',
                'rank': str(i),
                'name': coin['name'],
                'symbol': coin['symbol'],
                'change_24h': str(coin['change_24h'])
            })

        assert reader.fieldnames == expected_fieldnames
        assert rows == expected_rows


def test_console_output(capfd, report):
    console_output = ConsoleOutput(report)
    console_output.output()
    captured = capfd.readouterr()
    plain_output = Text.from_ansi(captured.out).plain
    assert 'Топ Роста и Падения' in plain_output
    assert f'{report.top_gainers[0]["name"]}' in plain_output
    assert f'{report.highest_volume["name"]}' in plain_output
    assert f'Капитал рынка: {report.total_market_cap_usd}' in plain_output


def test_console_output_columns(report, monkeypatch):
    printed = []
    monkeypatch.setattr(output_module.console, 'print', printed.append)
    ConsoleOutput(report).output()
    table = printed[0]
    assert table.columns[0].header == 'Рост'
    assert table.columns[1].header == 'За 24 часа'
    assert table.columns[2].header == 'Падение'
    assert table.columns[3].header == 'За 24 часа'
    assert list(table.columns[0].cells)[0] == report.top_gainers[0]['name']
    assert list(table.columns[1].cells)[0] == f"{report.top_gainers[0]['change_24h']:.2f}%"
    assert list(table.columns[2].cells)[0] == report.top_losers[0]['name']
    assert list(table.columns[3].cells)[0] == f"{report.top_losers[0]['change_24h']:.2f}%"
