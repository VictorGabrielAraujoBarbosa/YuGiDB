import subprocess
import os
import json
import shutil
import pytest


@pytest.fixture
def clean_decks():
    """Limpa pasta de decks antes e depois dos testes"""
    deck_folder = "data/decks"
    
    # Remove tudo antes do teste
    if os.path.exists(deck_folder):
        for file in os.listdir(deck_folder):
            file_path = os.path.join(deck_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(deck_folder, exist_ok=True)
    
    yield
    
    # Limpa depois do teste também
    if os.path.exists(deck_folder):
        for file in os.listdir(deck_folder):
            if file.endswith(".json"):
                file_path = os.path.join(deck_folder, file)
                try:
                    os.remove(file_path)
                except:
                    pass


def run_cli(commands):
    """Executa o CLI de verdade no terminal e retorna o output"""
    result = subprocess.run(
        ["python", "cli.py"],
        input=commands + "\nexit\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout


def test_e2e_create_deck_and_add_cards_real_cli(clean_decks):
    """E2E: Cria deck e adiciona cartas rodando o CLI real no terminal"""
    commands = """create_deck MeuDeck
add_card MeuDeck 10000
add_card MeuDeck 10001
show_deck MeuDeck"""
    
    output = run_cli(commands)
    
    # Verifica se o CLI printou as mensagens corretas
    assert "MeuDeck" in output
    assert "10000" in output
    assert "10001" in output


def test_e2e_search_and_create_deck_workflow_real_cli(clean_decks):
    """E2E: Busca cartas, cria deck e salva - workflow completo no CLI real"""
    commands = """search Blue
create_deck BlueDeck
add_card BlueDeck 10000
list_decks"""
    
    output = run_cli(commands)
    
    # Verifica se busca funcionou
    assert ":" in output  # Formato de resultado de busca: "id: nome"
    
    # Verifica se deck foi criado
    assert "BlueDeck" in output
    
    # Verifica que o deck aparece na listagem
    assert "Decks" in output or "BlueDeck" in output