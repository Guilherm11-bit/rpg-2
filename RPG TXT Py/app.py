from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = 'chave secreta'  

# Itens da loja
itens_loja = {
    "Poção de Cura": {"preço": 20.00, "estoque": 10},
    "Espada": {"preço": 50.00, "estoque": 5},
    "Escudo": {"preço": 30.00, "estoque": 5},
}

# Jogador com atributos iniciais
class Jogador:
    def __init__(self, nome, dinheiro_inicial=100):
        self.nome = nome
        self.hp = 100
        self.ataque = 10
        self.defesa = 5
        self.inventario = []
        self.dinheiro = dinheiro_inicial  # Adicionando o dinheiro inicial do jogador

    def usar_item(self, item):
        if item == "Poção de Cura" and item in self.inventario:
            cura = random.randint(15, 30)
            self.hp += cura
            self.inventario.remove(item)
        else:
            print(f"Você não tem {item} no inventário ou não pode usá-lo!")

    def adicionar_item(self, item):
        self.inventario.append(item)

    def remover_item(self, item):
        if item in self.inventario:
            self.inventario.remove(item)

    def exibir_status(self):
        return {
            "nome": self.nome,
            "hp": self.hp,
            "ataque": self.ataque,
            "defesa": self.defesa,
            "dinheiro": self.dinheiro,
            "inventario": self.inventario
        }

@app.route('/')
def index():
    # Se o jogador já estiver em sessão, não cria outro
    if 'jogador' not in session:
        return render_template('index.html', jogador=None)
    jogador = session['jogador']
    return render_template('index.html', jogador=jogador)

@app.route('/criar_jogador', methods=['POST'])
def criar_jogador():
    nome = request.form['nome']
    dinheiro_inicial = float(request.form['dinheiro_inicial'])
    jogador = Jogador(nome, dinheiro_inicial)
    session['jogador'] = jogador.exibir_status()
    return jsonify(jogador=jogador.exibir_status())

@app.route('/comprar_item', methods=['POST'])
def comprar_item():
    jogador_data = session.get('jogador')
    if not jogador_data:
        return jsonify(message="Jogador não encontrado."), 404

    jogador = Jogador(jogador_data['nome'], jogador_data['dinheiro'])
    jogador.hp = jogador_data['hp']
    jogador.ataque = jogador_data['ataque']
    jogador.defesa = jogador_data['defesa']
    jogador.inventario = jogador_data['inventario']

    item = request.json['item']
    quantidade = request.json['quantidade']
    
    if item not in itens_loja:
        return jsonify(message="Item não encontrado na loja."), 404
    
    total = itens_loja[item]['preço'] * quantidade
    if jogador.dinheiro < total:
        return jsonify(message="Dinheiro insuficiente!"), 400
    
    if itens_loja[item]['estoque'] < quantidade:
        return jsonify(message="Estoque insuficiente!"), 400
    
    # Atualizando o jogador
    jogador.dinheiro -= total
    jogador.adicionar_item(item)
    itens_loja[item]['estoque'] -= quantidade
    session['jogador'] = jogador.exibir_status()
    
    return jsonify(jogador=jogador.exibir_status(), message=f"Compra realizada! {quantidade}x {item}")

@app.route('/sortear_promocao', methods=['POST'])
def sortear_promocao():
    item_sorteado = random.choice(list(itens_loja.keys()))
    desconto = random.randint(10, 50)  # Desconto entre 10% e 50%
    itens_loja[item_sorteado]["preço"] *= (1 - desconto / 100)
    return jsonify(message=f"O item {item_sorteado} está com {desconto}% de desconto!")

if __name__ == '__main__':
    app.run(debug=True)
