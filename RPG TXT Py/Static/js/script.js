document.addEventListener("DOMContentLoaded", function() {
    const formCriarJogador = document.getElementById('formCriarJogador');
    const comprarButton = document.getElementById('comprarButton');
    const sortearPromocaoButton = document.getElementById('sortearPromocao');
    
    if (formCriarJogador) {
        formCriarJogador.addEventListener('submit', function(event) {
            event.preventDefault();
            const nome = formCriarJogador.nome.value;
            const dinheiro_inicial = formCriarJogador.dinheiro_inicial.value;
            
            fetch('/criar_jogador', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nome, dinheiro_inicial })
            })
            .then(response => response.json())
            .then(data => {
                window.location.reload();
            });
        });
    }

    if (comprarButton) {
        comprarButton.addEventListener('click', function() {
            const item = document.getElementById('itemComprar').value;
            const quantidade = document.getElementById('quantidadeComprar').value;

            fetch('/comprar_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ item, quantidade })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.reload();
            });
        });
    }

    if (sortearPromocaoButton) {
        sortearPromocaoButton.addEventListener('click', function() {
            fetch('/sortear_promocao', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            });
        });
    }
});
