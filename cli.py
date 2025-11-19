import cmd
import os
from models.database import CardDatabase
from models.deck import Deck
from storage.storage import save_deck, load_deck


class DeckManager:
    def __init__(self):
        self.decks = {}  # nome -> Deck

    def create(self, name):
        if name in self.decks:
            raise ValueError("Já existe um deck com esse nome.")
        self.decks[name] = Deck(name)

    def get(self, name):
        return self.decks.get(name)

    def list(self):
        return list(self.decks.keys())

    def delete(self, name):
        if name not in self.decks:
            raise ValueError("Deck não encontrado.")
        del self.decks[name]

    def add(self, name, card):
        deck = self.get(name)
        if not deck:
            raise ValueError("Deck não encontrado.")
        deck.add_card(card)

    def remove(self, name, card_id):
        deck = self.get(name)
        if not deck:
            raise ValueError("Deck não encontrado.")
        deck.remove_card(card_id)

    def rename(self, old, new):
        if old not in self.decks:
            raise ValueError("Deck original não encontrado.")
        if new in self.decks:
            raise ValueError("Já existe um deck com esse nome.")
        deck = self.decks.pop(old)
        deck.name = new
        self.decks[new] = deck


class CardCLI(cmd.Cmd):
    intro = "Sistema de Decks Yu-Gi-Oh - digite help para ver os comandos"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.db = CardDatabase()
        self.manager = DeckManager()

        # CARREGAMENTO AUTOMÁTICO
        decks_path = "data/decks"
        os.makedirs(decks_path, exist_ok=True)

        loaded = 0
        for filename in os.listdir(decks_path):
            if filename.endswith(".json"):
                name = filename.replace(".json", "")
                try:
                    deck = load_deck(name, self.db)
                    self.manager.decks[deck.name] = deck
                    loaded += 1
                except Exception as e:
                    print(f"[Aviso] Erro ao carregar {filename}: {e}")

        print(f"{loaded} deck(s) carregados automaticamente.")


    # CRIAR DECK

    def do_create_deck(self, name):
        """create_deck <nome> - cria um novo deck"""
        name = name.strip()
        if not name:
            print("Uso: create_deck <nome>")
            return

        try:
            self.manager.create(name)
            print(f"Deck '{name}' criado.")
        except ValueError as e:
            print(e)

    # LISTAR DECKS

    def do_list_decks(self, _):
        """list_decks - lista todos os decks"""
        decks = self.manager.list()
        if not decks:
            print("Nenhum deck disponível.")
        else:
            for d in decks:
                print("•", d)

    # MOSTRAR CARTAS DO DECK

    def do_show_deck(self, name):
        """show_deck <nome> - mostra o conteúdo do deck"""
        name = name.strip()

        if not name:
            print("Uso: show_deck <nome>")
            return

        deck = self.manager.get(name)
        if not deck:
            print("Deck não encontrado.")
            return

        print(f"Deck: {deck.name}")
        if not deck.cards:
            print("(vazio)")
            return

        for card in deck.cards:
            print(f"{card.id} — {card.name}")

    # APAGA O DECK

    def do_delete_deck(self, name):
        """delete_deck <nome> - apaga o deck"""
        name = name.strip()
        if not name:
            print("Uso: delete_deck <nome>")
            return

        try:
            self.manager.delete(name)
        except ValueError as e:
            print(e)
            return

        path = os.path.join("data/decks", f"{name}.json")
        if os.path.exists(path):
            os.remove(path)
            print(f"Deck '{name}' deletado e arquivo removido.")
        else:
            print(f"Deck '{name}' deletado (sem arquivo salvo).")

    # RENOMEAR DECK

    def do_rename_deck(self, args):
        """rename_deck <antigo> <novo> - renomeia um deck"""

        parts = args.split()
        if len(parts) != 2:
            print("Uso: rename_deck <antigo> <novo>")
            return

        old, new = parts
        old = old.strip()
        new = new.strip()

        if not old or not new:
            print("Os nomes não podem ser vazios.")
            return

        old_path = os.path.join("data/decks", f"{old}.json")
        new_path = os.path.join("data/decks", f"{new}.json")

        try:
            self.manager.rename(old, new)
        except ValueError as e:
            print(e)
            return

        # Renomeia arquivo se existir
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

        print(f"Deck renomeado de '{old}' para '{new}'.")

    # APAGAS APENAS AS CARTAS DO DECK

    def do_clear_deck(self, name):
        """clear_deck <nome> - remove todas as cartas do deck"""
        name = name.strip()
        if not name:
            print("Uso: clear_deck <nome>")
            return

        deck = self.manager.get(name)
        if not deck:
            print("Deck não encontrado.")
            return

        deck.cards = []
        print(f"Deck '{name}' esvaziado (todas as cartas removidas).")

    # PROCURA CARTAS

    def do_search(self, text):
        """search <texto> - busca cartas pelo nome"""
        text = text.strip()
        if not text:
            print("Uso: search <texto>")
            return

        results = self.db.search(text)
        if not results:
            print("Nenhuma carta encontrada.")
            return

        for c in results[:50]:
            print(f"{c.id}: {c.name}")

    # ADICIONA CARTA AO DECK

    def do_add_card(self, args):
        """add_card <deck> <id> - adiciona carta ao deck"""
        parts = args.split()
        if len(parts) != 2:
            print("Uso: add_card <deck> <id>")
            return

        deck_name, cid = parts
        try:
            cid = int(cid)
        except ValueError:
            print("ID inválido.")
            return

        card = self.db.get(cid)
        if not card:
            print("Carta não encontrada.")
            return

        try:
            self.manager.add(deck_name, card)
            print(f"Carta {cid} adicionada ao deck '{deck_name}'.")
        except ValueError as e:
            print(e)

    # REMOVE CARTA DO DECK

    def do_remove_card(self, args):
        """remove_card <deck> <id> - remove carta do deck"""
        parts = args.split()
        if len(parts) != 2:
            print("Uso: remove_card <deck> <id>")
            return

        deck_name, cid = parts
        try:
            cid = int(cid)
        except ValueError:
            print("ID inválido.")
            return

        try:
            self.manager.remove(deck_name, cid)
            print(f"Carta {cid} removida do deck '{deck_name}'.")
        except ValueError as e:
            print(e)

    # SALVA O DECK

    def do_save_deck(self, name):
        """save_deck <nome> - salva o deck"""
        name = name.strip()
        if not name:
            print("Uso: save_deck <nome>")
            return

        deck = self.manager.get(name)
        if not deck:
            print("Deck não encontrado.")
            return

        save_deck(deck)
        print(f"Deck '{name}' salvo")

    # SAI DO PROGRAMA

    def do_exit(self, _):
        """exit - sai do programa"""
        print("Saindo...")
        return True


def main():
    CardCLI().cmdloop()


if __name__ == "__main__":
    main()
