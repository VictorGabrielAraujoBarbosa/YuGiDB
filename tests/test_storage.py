import os
import json
import pytest
from unittest import mock
from models.deck import Deck
from storage.storage import save_deck, load_deck

DEFAULT_FOLDER = "data/decks"

class MockCard:
    def __init__(self, card_id):
        self.id = card_id

    def __eq__(self, outro):
        
        if isinstance(outro, MockCard):
            return self.id == outro.id
        
        return self.id == outro 

class MockDB:
    def __init__(self): 
        self.cards = {1: "card1", 2: "card2", 3: "card3"} 

    def get(self, card_id):
        return self.cards.get(card_id) 

@pytest.fixture
def deck():
    
    deck = Deck("test_deck")
    deck.add_card(MockCard(1)) 
    deck.add_card(MockCard(2))
    
    return deck

@pytest.fixture
def mock_db():
    return MockDB() 

def test_save_deck(tmp_path):
    
    deck = Deck("test_deck")
    deck.add_card(1)
    deck.add_card(2)

    folder = tmp_path / "decks"
    folder.mkdir()

    with mock.patch("builtins.open", mock.mock_open()) as mocked_open:

        save_deck(deck, folder=str(folder))

        caminho_esperado = os.path.join(str(folder), f"{deck.name}.json")
        mocked_open.assert_called_once_with(caminho_esperado, "w", encoding="utf-8")

        handle = mocked_open()
        dados = "".join(call.args[0] for call in handle.write.call_args_list)
        deck_json = json.loads(dados)

        assert deck_json["name"] == "test_deck"
        assert deck_json["cards"] == [1, 2]

def test_load_deck(deck, mock_db):
    
    deck_dict = {
        "name": deck.name,
        "cards": [1, 2]
    }
    
    with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(deck_dict))):
        
        deck_verdadeiro = load_deck("test_deck", mock_db) 
        
        assert deck_verdadeiro.name == deck.name
        assert len(deck_verdadeiro.cards) == 2
        assert "card1" in deck_verdadeiro.cards
        assert "card2" in deck_verdadeiro.cards