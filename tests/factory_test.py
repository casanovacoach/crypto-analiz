from modules.factory import ProviderFactory, OutputFactory

def test_provider_factory_create():
    expected = object()
    source = {
        'coingecko' : lambda: expected
    }
    provider = ProviderFactory(source)

    assert provider.create('coingecko') is expected


def test_output_factory_create():
    expected = object()
    output_format = {
        'JSON' : lambda: expected
    }
    output = OutputFactory(output_format)

    assert output.create('JSON') is expected