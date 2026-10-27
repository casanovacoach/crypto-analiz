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

    mocker.patch(
        "modules.main.ProviderFactory",
        return_value=provider_factory,
    )

    json_output_mock = mocker.patch("modules.main.JsonOutput")

    result = runner.invoke(
        app,
        [
            "--source", "coinmarketcap",
            "--output", "json",
            "--top", "3",
        ],
    )

    assert result.exit_code == 0, result.output

    provider_factory.create.assert_called_once_with(
        Source.COINMARKETCAP
    )
    provider.fetch_coins_data.assert_called_once_with()

    json_output_mock.assert_called_once()
    report = json_output_mock.call_args.args[0]

    assert len(report.top_gainers) == 3
    assert len(report.top_losers) == 3

    json_output_mock.return_value.output.assert_called_once_with()
