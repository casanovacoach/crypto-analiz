class ProviderFactory:

    def __init__(self, providers):
        self.providers = providers

    def create(self, source):
        return self.providers[source]()

class OutputFactory:
    def __init__(self, outputs):
        self.outputs = outputs

    def create(self, output_format):
        return self.outputs[output_format]()