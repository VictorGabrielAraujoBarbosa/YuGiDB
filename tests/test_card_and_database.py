import json
import pytest
from models.card import Card
from models.database import CardDatabase


# unit: Card inicializado com todos os campos — verifica atributos e representação
def test_card_full_fields():
    data = {
        "id": 123,
        "type": "monster",
        "name": "Blue-Eyes White Dragon",
        "localizedAttribute": "LIGHT",
        "effectText": "Huge dragon",
        "level": 8,
        "atk": 3000,
        "def": 2500,
        "properties": ["dragon", "effect"]
    }

    card = Card(data)

    assert card.id == 123
    assert card.type == "monster"
    assert card.name == "Blue-Eyes White Dragon"
    assert card.attribute == "LIGHT"
    assert card.effect == "Huge dragon"
    assert card.level == 8
    assert card.atk == 3000
    assert card.def_ == 2500
    assert "dragon" in card.properties
    assert "Blue-Eyes" in repr(card)


# unit: Card com campos opcionais ausentes — verifica valores padrão e lista vazia de properties
def test_card_missing_optional_fields():
    data = {"id": 45, "name": "Minimal Card"}

    card = Card(data)

    assert card.id == 45
    assert card.name == "Minimal Card"
    assert card.type is None
    assert card.attribute is None
    assert card.effect is None
    assert card.properties == []


# unit: Carrega arquivo JSON único representando uma carta — verifica carga no CardDatabase
def test_carddatabase_load_single_file(tmp_path):
    folder = tmp_path / "db"
    folder.mkdir()

    card_data = {"id": 1, "name": "Single Card"}
    file_path = folder / "1.json"
    file_path.write_text(json.dumps(card_data), encoding="utf-8")

    db = CardDatabase(path=str(folder))

    c = db.get(1)
    assert c is not None
    assert c.id == 1
    assert c.name == "Single Card"


# unit: Carrega arquivo JSON contendo lista de cartas — verifica múltiplos registros e busca por nome
def test_carddatabase_load_list_file(tmp_path):
    folder = tmp_path / "db"
    folder.mkdir()

    data = [
        {"id": 10, "name": "Alpha"},
        {"id": 11, "name": "Beta"}
    ]

    (folder / "cards.json").write_text(json.dumps(data), encoding="utf-8")

    db = CardDatabase(path=str(folder))

    assert db.get(10).name == "Alpha"
    assert db.get(11).name == "Beta"

    results = db.search("alpha")
    assert any("Alpha" in c.name for c in results)


# unit: Inicializar CardDatabase com pasta inexistente levanta FileNotFoundError
def test_carddatabase_missing_folder_raises(tmp_path):
    folder = tmp_path / "no_exist"

    with pytest.raises(FileNotFoundError):
        CardDatabase(path=str(folder))
