import pytest
from models.database import CardDatabase

@pytest.fixture(scope="class")
def database():
    db = CardDatabase()
    return db

class TestDatabase:
    def test_get_card_by_id(self, database):
        card_id = 16856
        card = database.get(card_id)
        assert card is not None
        assert card.name == "Fusão Definitiva"

    def test_searching_inexistent_card_returns_empty(self, database):
        result = database.search("13hnf093741gh09457gh-06h56ysaf") # nenhuma carta tem esse texto
        assert len(result) == 0 

    def test_database_loads_all_cards(self, database):
        assert len(database.search("")) > 10000 # retorna todas as cartas pq a string vazia é substring de qualquer string.