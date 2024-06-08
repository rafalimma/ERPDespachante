// // methods.js

// function Abacadastro() {
//     // Verificar se o formulário já está aberto
//     var existingForm = document.getElementById('cadastroForm');
    
//     // Se o formulário já estiver aberto, fechar
//     if (existingForm) {
//         existingForm.parentNode.removeChild(existingForm);
//         return;
//     }

//     // Criar um elemento div para conter o formulário de cadastro
//     var formContainer = document.createElement('div');
//     formContainer.id = 'cadastroForm';
//     formContainer.className = 'container custom-container mt-3'; // Adicionar margem superior

//     // Adicionar o formulário de cadastro ao div
//     formContainer.innerHTML = `
//         <form id="cadastroForm" action="{% url 'cadastro' %}" method="post" enctype="multipart/form-data"> 
//             <div class="mb-0">
//                 <label for="inputName" class="form-label">Nome</label>
//                 <input name="name" type="text" class="form-control" id="inputName" placeholder="Nome">
//             </div>
//             <div class="mb-1">
//                 <label for="inputCpfCnpj" class="form-label">CPF / CNPJ</label>
//                 <input name="cpfcnpj" type="number" class="form-control" id="inputCpfCnpj" placeholder="CPF / CNPJ">
//             </div>
//             <div class="mb-1">
//                 <label for="inputFones" class="form-label">Telefone</label>
//                 <input name="telefone" type="number" class="form-control" id="inputFones" placeholder="Telefone">
//             </div>
//             <button type="submit" class="btn btn-success">Salvar</button>
//             <button type="button" class="btn btn-secondary" onclick="FecharCadastro()">Fechar</button>
//         </form>
//     `;

//     // Inserir o div antes da tabela
//     var tableContainer = document.querySelector('table');
//     tableContainer.parentNode.insertBefore(formContainer, tableContainer);

//     // Adicionar um listener de evento para o envio do formulário
//     document.getElementById('cadastroForm').addEventListener('submit', function(event) {
//         // Impedir o comportamento padrão do formulário
//         event.preventDefault();
//         // Fechar o formulário após o envio
//         FecharCadastro();
//     });
// }

// // Função para fechar o formulário de cadastro
// function FecharCadastro() {
//     var formContainer = document.getElementById('cadastroForm');
//     if (formContainer) {
//         formContainer.parentNode.removeChild(formContainer);
//     }
// }

function exibirMensagem(mensagem, tipo='success') {
    // Define a classe de estilo com base no tipo de mensagem (pode ser 'success', 'warning', 'error', etc.)
    var classeEstilo = 'alert-' + tipo;

    // Atualiza o conteúdo da div de mensagem e define a classe de estilo
    $('#mensagem').html('<div class="alert ' + classeEstilo + '">' + 'cliente excluido' + '</div>');

    // Exibe a div de mensagem e define um temporizador para escondê-la após alguns segundos (por exemplo, 5 segundos)
    $('#mensagem').show().delay(4000).fadeOut();
}