class Card:
    def __init__(self, data):
        self.id = data["id"]
        self.type = data.get("type")
        self.name = data.get("name")
        self.attribute = data.get("localizedAttribute")
        self.effect = data.get("effectText")
        self.level = data.get("level")
        self.atk = data.get("atk")
        self.def_ = data.get("def")
        self.properties = data.get("properties", [])

    def __repr__(self):
        return f"{self.name} (ID: {self.id})"
