class User:
    def __init__(self, row: int, equipment_id: str, user_id: str, username: str) -> None:
        self._row: int = row
        self._equipment_id: str = equipment_id
        self._user_id: str = user_id
        self._username: str = username
        self._game_score: int = 0
        self._has_hit_base: bool = False

    @property
    def row(self) -> int:
        return self._row

    @property
    def equipment_id(self) -> str:
        return self._equipment_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def game_score(self) -> int:
        return self._game_score

    @game_score.setter
    def game_score(self, score: int) -> None:
        self._game_score = score

    @property
    def has_hit_base(self) -> bool:
        return self._has_hit_base

    @has_hit_base.setter
    def has_hit_base(self, value: bool) -> None:
        self._has_hit_base = value

    def __str__(self) -> str:
        return f"Username: {self._username}\nEquipment ID: {self._equipment_id}\nUser ID: {self._user_id}\nGame Score: {self._game_score}\nHas Hit Base: {self._has_hit_base}\n"
