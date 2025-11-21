import os
import json
from models.deck import Deck
from storage.storage import save_deck, load_deck
from models.database import CardDatabase


# e2e: Integração real de salvar e carregar um deck usando CardDatabase e arquivos no disco
def test_save_and_load_integration(tmp_path):
    db_folder = tmp_path / "db"
    db_folder.mkdir()

    card = {"id": 7, "name": "Test Card"}
    (db_folder / "7.json").write_text(json.dumps(card), encoding="utf-8")

    db = CardDatabase(path=str(db_folder))

    deck = Deck("integration_deck")
    deck.add_card(7)

    out_folder = tmp_path / "out"
    out_folder.mkdir()

    save_deck(deck, folder=str(out_folder))

    loaded = load_deck("integration_deck", db, folder=str(out_folder))

    assert loaded.name == "integration_deck"
    assert len(loaded.cards) == 1
    assert loaded.cards[0].name == "Test Card"
