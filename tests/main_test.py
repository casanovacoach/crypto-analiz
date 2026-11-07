from unittest.mock import MagicMock

from typer.testing import CliRunner

from modules.main import app
from modules.typer_option import Source


runner = CliRunner()


def test_app(mocker, bitcoin, ethereum, dogcoin):

    coins = [bitcoin, ethereum, dogcoin]


    provider = mocker.MagicMock()
    provider.fetch_coins_data.return_value = coins

    provider_factory = mocker.MagicMock()
    provider_factory.create.return_value = provider
    storage_mock = MagicMock()
    storage_factory_mock = MagicMock()
    mocker.patch("modules.main.StorageFactory",
                 return_value=storage_factory_mock)

    storage_factory_mock.create.return_value=storage_mock
    mocker.patch(
        "modules.main.ProviderFactory",
        return_value=provider_factory,
    )

    json_output_mock = mocker.patch("modules.main.JsonOutput")

    result = runner.invoke(
        app,
        [
            "main",
            "--source", "coinmarketcap",
            "--output", "json",
            "--top", "2",
        ],
    )

    assert result.exit_code == 0, result.output

    provider_factory.create.assert_called_once_with(
        Source.COINMARKETCAP
    )
    provider.fetch_coins_data.assert_called_once_with()

    json_output_mock.assert_called_once()
    report = json_output_mock.call_args.args[0]

    assert len(report.top_gainers) == 2
    assert len(report.top_losers) == 2
    storage_factory_mock.create.assert_called_once()
    storage_mock.save.assert_called_once()
    saved_agrs = storage_mock.save.call_args.args[0]
    assert saved_agrs["coins"] == coins
    assert saved_agrs["report"] == report.__dict__

    json_output_mock.return_value.output.assert_called_once_with()
