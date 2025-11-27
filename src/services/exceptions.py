class AllOperatorsBusyError(Exception):
    def __init__(self, message: str = "Все операторы заняты. Попробуйте позже.") -> None:
        super().__init__(message)


class SourceNotFoundError(Exception):
    def __init__(self, source_name: str) -> None:
        super().__init__(f"Источник с именем '{source_name}' не найден.")
        self.source_name = source_name
