class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card_id, amount=1):
        removed = 0
        for card in self.cards[:]:
            if card == card_id and removed < amount:
                self.cards.remove(card)
                removed += 1

    def to_dict(self):
        return {
            "name": self.name,
            "cards": [c for c in self.cards]
        }

    def __repr__(self):
        return f"<Deck {self.name} ({len(self.cards)} cartas)>"
