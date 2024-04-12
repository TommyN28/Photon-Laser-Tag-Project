class User:
    def __init__(self, row, equipment_id, user_id, username) -> None:
        self.row = row
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.username = username
        self.game_score = 0
        self.has_hit_base = False

    def __str__(self) -> str:
        return f"Username: {self.username}\nEquipment ID: {self.equipment_id}\nUser ID: {self.user_id}\nGame Score: {self.game_score}\nHas Hit Base: {self.has_hit_base}\n\n"
