class Lexer:

    def __init__(self, code: str):
        self.code = code

    async def cleanup(self):
        self.code = self.code.replace('\r\n', '\n')