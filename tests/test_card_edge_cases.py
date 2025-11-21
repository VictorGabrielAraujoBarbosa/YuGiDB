import json
import pytest
from models.card import Card
from models.database import CardDatabase
from models.deck import Deck


def test_card_with_only_id():
    # carta com o mínimo possível - só tem ID
    data = {"id": 999}
    
    card = Card(data)
    
    assert card.id == 999
    assert card.name is None
    assert card.type is None
    assert card.properties == []


def test_card_with_zero_stats():
    # carta com ATK/DEF zerados (válido no Yu-Gi-Oh!)
    data = {
        "id": 42,
        "name": "Weak Monster",
        "atk": 0,
        "def": 0,
        "level": 1
    }
    
    card = Card(data)
    
    assert card.atk == 0  # zero é diferente de None
    assert card.def_ == 0
    assert card.level == 1


def test_search_with_none_name(tmp_path):
    # search não deve quebrar se carta não tem nome
    folder = tmp_path / "db"
    folder.mkdir()
    
    data = {"id": 1, "effectText": "Cool effect"}
    (folder / "1.json").write_text(json.dumps(data), encoding="utf-8")
    
    db = CardDatabase(path=str(folder))
    results = db.search("cool")
    
    assert len(results) == 1
    assert results[0].id == 1


def test_search_with_none_effect(tmp_path):
    # search não deve quebrar se carta não tem efeito
    folder = tmp_path / "db"
    folder.mkdir()
    
    data = {"id": 2, "name": "Normal Monster"}
    (folder / "2.json").write_text(json.dumps(data), encoding="utf-8")
    
    db = CardDatabase(path=str(folder))
    results = db.search("normal")
    
    assert len(results) == 1
    assert results[0].name == "Normal Monster"


def test_search_empty_query(tmp_path):
    # buscar string vazia deve retornar tudo
    folder = tmp_path / "db"
    folder.mkdir()
    
    data = [
        {"id": 1, "name": "Card A"},
        {"id": 2, "name": "Card B"}
    ]
    (folder / "list.json").write_text(json.dumps(data), encoding="utf-8")
    
    db = CardDatabase(path=str(folder))
    results = db.search("")
    
    assert len(results) == 2


def test_get_missing_card(tmp_path):
    # get() com ID que não existe deve retornar None
    folder = tmp_path / "db"
    folder.mkdir()
    
    data = {"id": 1, "name": "Exists"}
    (folder / "1.json").write_text(json.dumps(data), encoding="utf-8")
    
    db = CardDatabase(path=str(folder))
    result = db.get(99999)
    
    assert result is None


def test_deck_remove_more_than_available():
    # tentar remover 5 cópias quando só tem 2
    deck = Deck("test")
    deck.add_card(1)
    deck.add_card(1)
    
    deck.remove_card(1, amount=5)
    
    assert 1 not in deck.cards
    assert len(deck.cards) == 0


def test_deck_to_dict_preserves_duplicates():
    # to_dict deve manter cartas duplicadas na lista
    deck = Deck("dupes")
    deck.add_card(7)
    deck.add_card(7)
    deck.add_card(7)
    
    result = deck.to_dict()
    
    assert result["cards"].count(7) == 3
    assert len(result["cards"]) == 3
