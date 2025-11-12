import json
import os

class BookStoreInvetory:
    def __init__(self, json_file="recommendations.json"):
        self.inventory = {}
        self.json_file = json_file # Armazena o nome do arquivo para gravação
        self.recommendations_data = self._load_recommendations()
    
    # ----------------------------------------------------
    # MÉTODOS DE CARREGAMENTO E GRAVAÇÃO DE JSON (I/O)
    # ----------------------------------------------------
    def _load_recommendations(self):
        if not os.path.exists(self.json_file):
            print(f"ERRO: Arquivo de recomendações '{self.json_file}' não encontrado.")
            return {}
            
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"ERRO: O arquivo '{self.json_file}' está mal formatado (JSON inválido).")
            return {}

    # NOVO MÉTODO PRIVADO: Persiste as alterações no arquivo JSON
    def _save_recommendations(self):
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                # Usa indent=4 para formatar o JSON de forma legível
                json.dump(self.recommendations_data, f, indent=4, ensure_ascii=False)
            print(f"Catálogo de recomendações salvo em '{self.json_file}'.")
            return True
        except IOError:
            print(f"ERRO: Não foi possível salvar o arquivo '{self.json_file}'.")
            return False

    # ----------------------------------------------------
    # MÉTODOS CRUD NO JSON (Recomendação)
    # ----------------------------------------------------

    def add_genre_recommendation(self, genre, book_title):
        """Adiciona um livro a um gênero (ou cria o gênero se não existir)."""
        genre = genre.lower()
        if genre not in self.recommendations_data:
            self.recommendations_data[genre] = []

        if book_title not in self.recommendations_data[genre]:
            self.recommendations_data[genre].append(book_title)
            self._save_recommendations()
            return True
        return False

    def update_recommendation(self, genre, old_title, new_title):
        """Atualiza o título de um livro em um gênero."""
        genre = genre.lower()
        if genre in self.recommendations_data:
            try:
                # Encontra o índice do livro antigo na lista e o substitui
                index = self.recommendations_data[genre].index(old_title)
                self.recommendations_data[genre][index] = new_title
                self._save_recommendations()
                return True
            except ValueError:
                print(f"ERRO: Livro '{old_title}' não encontrado no gênero '{genre}'.")
        return False
        
    def delete_recommendation(self, genre, book_title=None):
        """
        Deleta um livro específico ou o gênero inteiro.
        Se book_title for None, deleta o gênero inteiro.
        """
        genre = genre.lower()
        if genre not in self.recommendations_data:
            return False
            
        if book_title:
            # Deleta um livro específico
            try:
                self.recommendations_data[genre].remove(book_title)
                # Se o gênero ficar vazio, deleta o gênero inteiro para limpar
                if not self.recommendations_data[genre]:
                    del self.recommendations_data[genre]
                self._save_recommendations()
                return True
            except ValueError:
                print(f"Livro '{book_title}' não encontrado para remoção em '{genre}'.")
                return False
        else:
            # Deleta o gênero inteiro
            del self.recommendations_data[genre]
            self._save_recommendations()
            return True
        
        return False

    # ----------------------------------------------------
    # MÉTODOS EXISTENTES (Inventário e Recomendação)
    # ----------------------------------------------------

    def addBook(self, title, quantity):
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def checkQuantity(self, title):
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
        
        # O catálogo é lido de self.recommendations_data
        recomendations = self.recommendations_data 
        
        results = []
        
        for key, books in recomendations.items():
            if key in desc_lower:
                results.extend(books) 
        
        if not results:
            return "Sem recomendações para você no momento."
       
        return list(set(results))

if __name__ == "__main__":
    
    # Certifique-se de que o recommendations.json existe antes de rodar!
    bookstore = BookStoreInvetory()
    
    print("\n\n--- TESTE CRUD NO CATÁLOGO JSON ---")
    
    # 1. CREATE (Adicionar um novo livro e um novo gênero)
    #print("1. Adicionando 'A Desolação de Smaug' (Fantasia):", 
    #      bookstore.add_genre_recommendation("fantasia", "A Desolação de Smaug"))
    # print("1. Criando novo gênero 'Poesia' e adicionando 'Ode Marítima':", 
    #      bookstore.add_genre_recommendation("poesia", "Ode Marítima de Álvaro de Campos"))

    # 2. UPDATE (Atualizar um título)
    # print("2. Atualizando 'O Nome do Vento' para 'O Medo do Sábio' (Fantasia):", 
    #      bookstore.update_recommendation("fantasia", "O Nome do Vento", "O Medo do Sábio"))

    # 3. DELETE (Deletar um livro específico)
    # print("3. Deletando 'O Código Da Vinci' (Mistério):", 
    #      bookstore.delete_recommendation("mistério", "O Código Da Vinci"))
          
    # 4. DELETE (Deletar um gênero inteiro)
    # print("4. Deletando o gênero 'Poesia' inteiro:", 
    #      bookstore.delete_recommendation("poesia")) 

    # print("\n>>> Após o CRUD, o arquivo 'recommendations.json' foi atualizado. Verifique o arquivo.")
    # print("Chaves de gênero restantes:", list(bookstore.recommendations_data.keys()))

    # bookstore.add_genre_recommendation("terror cósmico", " Chamado de Cthulhu")
    # bookstore.update_recommendation("terror cósmico", " Chamado de Cthulhu", "O  Chamado de Cthulhu")
    
    print("\n--- TESTE DE RECOMENDAÇÃO ---")
    recomendations = bookstore.recommendBooks("Quero um livro de terror cósmico.")
    print("Recomendações:", recomendations)