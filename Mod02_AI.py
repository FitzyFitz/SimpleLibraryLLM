import json
import os # Importamos 'os' para manipulação básica de caminhos de arquivo

class BookStoreInvetory:
    # O construtor é ajustado para carregar o inventário e o catálogo de recomendações
    def __init__(self, json_file="recommendations.json"):
        self.inventory = {}
        # Chama a função que lê o arquivo JSON
        self.recommendations_data = self._load_recommendations(json_file)
    
    # Novo método privado para carregar o arquivo JSON
    def _load_recommendations(self, json_file):
        # Verifica se o arquivo existe antes de tentar abrir
        if not os.path.exists(json_file):
            print(f"ERRO: Arquivo de recomendações '{json_file}' não encontrado.")
            return {}
            
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"ERRO: O arquivo '{json_file}' está mal formatado (JSON inválido).")
            return {}

    def addBook(self, title, quantity):
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def checkQuantity(self, title):
        # Retorna 0 se o título não estiver no inventário
        return self.inventory.get(title, 0)

    def removeBook(self, title, quantity):
        if title in self.inventory and self.inventory[title] >= quantity:
            self.inventory[title] -= quantity
            if self.inventory[title] == 0:
                del self.inventory[title]
            return True
        return False
        
    def listInventory(self):
        print("\n--- Inventário Atual da Livraria ---")
        if not self.inventory:
            print("O inventário está vazio.")
            return
        for title, quantity in self.inventory.items():
            print(f"Título: {title} | Quantidade: {quantity}")
        print("------------------------------------\n")

    def recommendBooks(self, description):
        desc_lower = description.lower()
        
        # Usa o dicionário carregado do JSON
        recomendations = self.recommendations_data 
        
        results = []
        
        for key, books in recomendations.items():
            if key in desc_lower:
                results.extend(books) 
        
        if not results:
            return "Sem recomendações para você no momento."
       
        # Remove duplicatas e retorna a lista
        return list(set(results))

if __name__ == "__main__":
    bookstore = BookStoreInvetory()
    
    # Verificação do JSON
    if not bookstore.recommendations_data:
        print("Sistema de recomendação inativo devido ao erro no JSON.")
    
    print("\n--- Teste de Inventário e Recomendação ---")
    
    # Inicialização do Inventário
    bookstore.addBook("Sapiens: Uma Breve História da Humanidade", 5)
    bookstore.addBook("Duna", 3)
    bookstore.addBook("O Hobbit de J.R.R. Tolkien", 1) # Note o nome completo do título
    bookstore.addBook("O Senhor dos Anéis", 2)
    bookstore.addBook("Harry Potter e a Pedra Filosofal", 4)
    bookstore.addBook("As Aventuras de Sherlock Holmes", 3)
    
    # Teste 1: Busca por múltiplas palavras-chave (Aventura e Fantasia)
    recomendations_multi = bookstore.recommendBooks("Quero uma aventura de fantasia.")
    print("\nRecomendações (Aventura de Fantasia):")
    # Imprime a lista de recomendações
    for rec in recomendations_multi:
        print(f" - {rec}")

    # Exemplo de teste de remoção
    bookstore.removeBook("Duna", 3)
    print("\n--- Após remover 3 unidades de Duna ---")
    bookstore.listInventory()