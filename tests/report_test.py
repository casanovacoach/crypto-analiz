from modules.report import Report


def test_report_coin(mocker,
                     data_coin,
                     top_gainers,
                     top_losers,
                     market_cap,
                     top_value_coin):

    mock_datetime = mocker.patch('modules.report.datetime.datetime')
    mock_datetime.now.return_value.strftime.return_value = "2002-10-27 05:00:01"

    report = Report(data_coin,
                    top_gainers,
                    top_losers,
                    market_cap,
                    top_value_coin)

    assert report.generated_at == "2002-10-27 05:00:01"
    assert report.total_coins_analyzed == len(data_coin)
    assert report.total_market_cap_usd == market_cap

    assert report.highest_volume == {
        "name": top_value_coin.name,
        "symbol": top_value_coin.symbol,
        "volume_usd": top_value_coin.volume,
    }

    assert report.top_gainers == [
        {
        "name": coin.name,
        "symbol": coin.symbol,
        "change_24h": round(coin.change_24h, 2)
        }
        for coin in top_gainers ]

    assert report.top_losers == [
        {
        "name": coin.name,
        "symbol": coin.symbol,
        "change_24h": round(coin.change_24h, 2)
        }
        for coin in top_losers ]