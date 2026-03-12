class ErrorReporter:

    def __init__(self):
        self.errori = []
        self.warnings = []

    def add(self, msg: str):
        self.errori.append(msg)

    def extend(self, lista_errori: list):
        self.errori.extend(lista_errori)

    def extend_errors(self, lista_errori: list):
        self.errori.extend(lista_errori)

    def extend_warnings(self, lista_warnings: list):
        self.warnings.extend(lista_warnings)

    def has_errors(self) -> bool:
        return len(self.errori) > 0

    def get_text(self) -> str:
        return "\n".join(self.errori)

    def get_error_text(self) -> str:
        return "\n".join(self.errori)

    def get_warning_text(self) -> str:
        return "\n".join(self.warnings)
