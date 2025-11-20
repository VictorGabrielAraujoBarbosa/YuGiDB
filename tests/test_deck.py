import pytest
from models.deck import Deck

@pytest.fixture(scope="class")
def dados():

    nome = "deck"
    cartas = [1, 2, 3]
    return {"nome": nome, "cartas": cartas}

class TestDeck:

    def test_create_empty_deck_with_name(self, dados):

        deck = Deck(dados["nome"])

        assert deck.name == dados["nome"]
        assert deck.cards == []

    def test_adding_multiple_cards(self, dados):

        deck = Deck(dados["nome"])

        for carta in dados["cartas"]:
            deck.add_card(carta)

        assert deck.cards == dados["cartas"]
        assert len(deck.cards) == 3

    def test_remove_card_from_id(self, dados):

        deck = Deck(dados["nome"])

        for carta in dados["cartas"]:
            deck.add_card(carta)

        deck.remove_card(1)

        assert 1 not in deck.cards
        assert 2 in deck.cards
        assert 3 in deck.cards
        assert len(deck.cards) == 2
    


    def test_convert_deck_to_dictionary(self, dados):

        deck = Deck(dados["nome"])

        for carta in dados["cartas"]:
            deck.add_card(carta)

        dicionario_esperado = {
            "name": dados["nome"],
            "cards": dados["cartas"]
        }

        assert deck.to_dict() == dicionario_esperado

    def test_representacao_como_string(self, dados):

        deck = Deck(dados["nome"])

        for carta in dados["cartas"]:
            deck.add_card(carta)

        string_esperada = f"<Deck {dados['nome']} (3 cartas)>"
        
        assert deck.__repr__() == string_esperada