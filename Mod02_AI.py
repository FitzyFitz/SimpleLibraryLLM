class BookStoreInvetory:
    def __init__(self):
        self.inventory = {}
    
    def addBook(self, title, quantity):
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def checkQuantity(self, title):
        if title in self.inventory:
            return self.inventory.get(title, 0)
        else:
            return 0

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

    # --- MÉTODO recommendBooks---
    def recommendBooks(self, description):
        desc_lower = description.lower()
        
        recomendations = {
           'aventura': ['O Hobbit de J.R.R. Tolkien', 'A Ilha do Tesouro'],
           'mistério': ['As Aventuras de Sherlock Holmes', 'O Código Da Vinci'],
           'romance': ['Orgulho e Preconceito de Jane Austen'],
           'ficção científica': ['Duna de Frank Herbert', 'Fundação de Isaac Asimov'],
           'fantasia': ['Harry Potter e a Pedra Filosofal', 'O Senhor dos Anéis', 'O Nome do Vento'],
           'história': ['Sapiens: Uma Breve História da Humanidade']
       }
       
        results = []
       
        for key, books in recomendations.items():
            if key in desc_lower:
                results.extend(books) 
       
        if not results:
            return "Sem recomendações para você no momento."
       
        return list(set(results))
# ----------------------------------------

if __name__ == "__main__":
    bookstore = BookStoreInvetory()
    bookstore.addBook("Sapiens: Uma Breve História da Humanidade", 5)
    bookstore.addBook("Duna", 3)
    bookstore.addBook("O Hobbit", 1)
    bookstore.addBook("O Senhor dos Anéis", 2)
    bookstore.addBook("Harry Potter e a Pedra Filosofal", 4)
    bookstore.addBook("As Aventuras de Sherlock Holmes", 3)
    
    # Teste 1: Busca por ficção científica
    # recomendations_ficcaoCientifica = bookstore.recommendBooks("Este livro é de ficção científica.")
    # print("Recomendações (Ficção Científica):")
    # print(recomendations_ficcaoCientifica) 

    # Teste 2: Busca por múltiplas palavras-chave
    recomendations = bookstore.recommendBooks("Quero uma aventura de fantasia.")
    print("Recomendações:")
    print(recomendations)