from contexts.data_generator_context import DataGeneratorContext


class Summarize:
    def __init__(self, context: DataGeneratorContext):
        self._context = context

    def summarize(self):
        raise NotImplementedError

    @property
    def context(self):
        return self._context
