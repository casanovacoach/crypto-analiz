from typer.testing import CliRunner

from modules.main import app
from modules.typer_option import Source, OutputFormat


runner = CliRunner()


def test_app(mocker, bitcoin, ethereum, dogcoin):
    # Подготавливаем тестовые монеты
    coins = [bitcoin, ethereum, dogcoin]

    # Создаём поддельный API-провайдер
    provider = mocker.MagicMock()
    provider.fetch_coins_data.return_value = coins

    # Создаём поддельную фабрику провайдеров
    provider_factory = mocker.MagicMock()
    provider_factory.create.return_value = provider

    mocker.patch(
        "modules.main.ProviderFactory",
        return_value=provider_factory,
    )

    # Создаём поддельный обработчик вывода
    output_handler = mocker.MagicMock()

    # Создаём поддельную фабрику форматов вывода
    output_factory = mocker.MagicMock()
    output_factory.create.return_value = output_handler

    mocker.patch(
        "modules.main.OutputFactory",
        return_value=output_factory,
    )

    # Запускаем CLI-команду
    result = runner.invoke(
        app,
        [
            "--source", "coinmarketcap",
            "--output", "json",
            "--top", "3",
        ],
    )

    # Проверяем результат
    assert result.exit_code == 0, result.output

    provider_factory.create.assert_called_once_with(
        Source.COINMARKETCAP
    )
    provider.fetch_coins_data.assert_called_once_with()

    output_factory.create.assert_called_once_with(
        OutputFormat.JSON
    )
    output_handler.output.assert_called_once_with()