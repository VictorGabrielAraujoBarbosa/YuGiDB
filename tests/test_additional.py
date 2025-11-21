import json
import os
import pytest
from models.deck import Deck
from models.card import Card
from models.database import CardDatabase
from storage.storage import save_deck, load_deck


class MockCard:
    def __init__(self, card_id):
        self.id = card_id

    def __eq__(self, other):
        if isinstance(other, MockCard):
            return self.id == other.id
        return self.id == other


class MockDB:
    def __init__(self, available=None):
        self.available = available or {}

    def get(self, cid):
        return self.available.get(cid)


# unit: Adiciona objetos ao deck e remove usando id
def test_deck_add_and_remove_objects():
    deck = Deck("obj_deck")
    a = MockCard(1)
    b = MockCard(2)

    deck.add_card(a)
    deck.add_card(b)

    deck.remove_card(1)

    assert all(getattr(c, "id", c) != 1 for c in deck.cards)
    assert len(deck.cards) == 1


# unit: to_dict retorna cópia dos cards — modificações no dict retornado não afetam o objeto
def test_deck_to_dict_is_copy():
    deck = Deck("copy_deck")
    deck.add_card(1)
    deck.add_card(2)

    d = deck.to_dict()
    d["cards"][0] = 999

    assert deck.cards[0] == 1


# unit: Representação string do deck vazio contém '0 cartas'
def test_deck_repr_empty():
    deck = Deck("empty")
    assert "0 cartas" in repr(deck)


# unit: Remover carta inexistente não altera o deck
def test_remove_nonexistent_card_no_change():
    deck = Deck("no_change")
    deck.add_card(1)
    deck.add_card(2)

    deck.remove_card(99)

    assert deck.cards == [1, 2]


# unit: save_deck escreve arquivo JSON no disco com conteúdo esperado
def test_save_deck_writes_file(tmp_path):
    deck = Deck("save_test")
    deck.add_card(1)
    deck.add_card(2)

    out = tmp_path / "out"
    out.mkdir()

    save_deck(deck, folder=str(out))

    path = os.path.join(str(out), "save_test.json")
    assert os.path.exists(path)

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["name"] == "save_test"
    assert data["cards"] == [1, 2]


# unit: load_deck pula cartas não encontradas no DB — apenas carrega as existentes
def test_load_deck_skips_missing_cards(tmp_path):
    deck_dict = {"name": "missing_cards", "cards": [1, 2, 3]}
    folder = tmp_path / "in"
    folder.mkdir()

    (folder / "missing_cards.json").write_text(json.dumps(deck_dict), encoding="utf-8")

    mock_db = MockDB(available={2: "card2"})

    loaded = load_deck("missing_cards", mock_db, folder=str(folder))

    assert loaded.name == "missing_cards"
    assert len(loaded.cards) == 1
    assert "card2" in loaded.cards

# unit: Representação de Card com nome ausente ainda inclui ID na string
def test_card_repr_with_none_name():
    c = Card({"id": 999})
    assert "(ID: 999)" in repr(c)


# unit: Busca no CardDatabase é case-insensitive e parcial
def test_carddatabase_search_partial_case_insensitive(tmp_path):
    folder = tmp_path / "db"
    folder.mkdir()

    data = [
        {"id": 10, "name": "Alpha Card"},
        {"id": 11, "name": "Beta Card"}
    ]

    (folder / "list.json").write_text(json.dumps(data), encoding="utf-8")

    db = CardDatabase(path=str(folder))

    results = db.search("alpha")
    assert any("Alpha" in c.name for c in results)
