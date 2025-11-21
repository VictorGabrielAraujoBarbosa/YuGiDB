import pytest
import io
import sys
from unittest.mock import MagicMock, patch
from cli import CardCLI

# --- FIXTURES (Configurações iniciais) ---

@pytest.fixture
def mock_dependencies(mocker):
    """
    Mocka (simula) as dependências externas para que o teste
    não precise de banco de dados real nem criar arquivos no disco.
    """
    # Mock do Banco de Dados
    mock_db_class = mocker.patch('cli.CardDatabase')
    mock_db_instance = mock_db_class.return_value
    
    # Mock do Storage (Salvar/Carregar)
    mocker.patch('cli.save_deck')
    mocker.patch('cli.load_deck')
    
    # Mock de operações de SO (para não criar pasta data/decks de verdade)
    mocker.patch('os.makedirs')
    mocker.patch('os.listdir', return_value=[]) # Simula pasta vazia
    mocker.patch('os.remove')
    mocker.patch('os.path.exists', return_value=True)
    
    return mock_db_instance

@pytest.fixture
def run_cli(capsys):
    """
    Helper para rodar a CLI com um texto de entrada simulado
    e retornar a saída capturada.
    """
    def _run(input_text):
        # Prepara a entrada simulada (Stdin)
        with patch('sys.stdin', io.StringIO(input_text)):
            cli = CardCLI()
            # use_rawinput=False é crucial para testar módulo cmd com StringIO
            cli.use_rawinput = False 
            try:
                cli.cmdloop()
            except SystemExit:
                pass # Ignora saída do sistema se houver
        
        # Captura o que foi printado (Stdout)
        return capsys.readouterr().out
    return _run

# --- TESTES E2E ---

def test_fluxo_criar_listar_sair(run_cli):
    """
    Cenário: Usuário cria um deck, lista e sai.
    """
    input_commands = """
    create_deck MeuDeckDragon
    list_decks
    exit
    """
    output = run_cli(input_commands)
    
    assert "Deck 'MeuDeckDragon' criado." in output
    assert "• MeuDeckDragon" in output
    assert "Saindo..." in output

def test_erro_criar_deck_duplicado(run_cli):
    """
    Cenário: Usuário tenta criar dois decks com mesmo nome.
    """
    input_commands = """
    create_deck Exodia
    create_deck Exodia
    exit
    """
    output = run_cli(input_commands)
    
    assert "Deck 'Exodia' criado." in output
    assert "Já existe um deck com esse nome." in output

def test_adicionar_e_mostrar_cartas(run_cli):
    """
    Cenário: Cria deck, adiciona carta e verifica se ela aparece no show.
    """

    input_commands = """
    create_deck blue_eyes
    add_card blue_eyes 15579
    show_deck blue_eyes
    exit
    """
    output = run_cli(input_commands)
    
    assert "Carta 15579 adicionada ao deck 'blue_eyes'." in output
    assert "Deck: blue_eyes" in output
    assert "15579 — Rivais Destinados" in output

def test_remover_deck(run_cli):
    """
    Cenário: Usuário apaga um deck existente.
    """
    input_commands = """
    create_deck Lixo
    delete_deck Lixo
    list_decks
    exit
    """
    output = run_cli(input_commands)
    
    assert "Deck 'Lixo' deletado" in output
    assert "Nenhum deck disponível." in output

def test_comando_invalido_help(run_cli):
    """
    Cenário: Digitar algo que não existe.
    """
    input_commands = """
    voar_alto
    exit
    """
    output = run_cli(input_commands)
    
    # O módulo cmd padrão imprime algo como "*** Unknown syntax: voar_alto"
    # ou simplesmente ignora/printa help dependendo da config, 
    # mas geralmente imprime mensagem de erro padrão.
    assert "Unknown syntax: voar_alto" in output

def test_renomear_deck(run_cli):
    """
    Cenário: Renomear um deck e verificar listagem.
    """
    input_commands = """
    create_deck Antigo
    rename_deck Antigo Novo
    list_decks
    exit
    """
    output = run_cli(input_commands)

    assert "Deck renomeado de 'Antigo' para 'Novo'." in output
    assert "• Novo" in output
    assert output.count("Antigo") == 2  # Garante que o velho sumiu