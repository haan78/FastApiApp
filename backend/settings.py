from lib.ENV import ENV
class Settings:
    DBCONN: str
    DBNAME: str
    SESSIONTIME: int
    JWTKEY: str

    def __init__(self) -> None:
        self.DBCONN: str = ENV("DBCONN", str)
        self.DBNAME: str = ENV("DBNAME", str)
        self.SESSIONTIME: int = ENV("SESSIONTIME", int, False, 500)
        self.JWTKEY: str = ENV("JWTKEY", str)
