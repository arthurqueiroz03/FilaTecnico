document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('form-agendamento');
  const msgSucesso = document.getElementById('msg-sucesso');
  const botaoOk = document.getElementById('ok');

  // Apagar agendamento ao clicar na linha da tabela
  document.querySelectorAll('.btn-apagar').forEach(btn => {
    btn.addEventListener('click', function (event) {
      event.stopPropagation(); // evita clique no pai
      const id = this.dataset.id;
      if (confirm("Deseja realmente apagar esse agendamento?")) {
        fetch(`/apagar/${id}`, { method: 'POST' })
          .then(response => {
            if (response.ok) {
              this.closest('.agendamento').remove();
            } else {
              alert('Erro ao apagar agendamento.');
            }
          });
      }
    });
  });

  // Submissão do formulário
  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault(); // ← Importante! Para evitar recarregar a página
      const formData = new FormData(form);

      fetch('/agendar', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (response.ok) {
          msgSucesso.style.display = 'block';
          form.reset();
        } else {
          alert('Erro ao agendar. Tente novamente.');
        }
      })
      .catch(error => {
        console.error('Erro:', error);
        alert('Erro de conexão.');
      });
    });
  }

  // Botão "ok" na mensagem de sucesso
  if (botaoOk) {
    botaoOk.addEventListener('click', function() {
      msgSucesso.style.display = 'none';
    });
  }

  // Filtro de pesquisa na tabela
  const campoPesquisa = document.getElementById('pesquisa');
  if (campoPesquisa) {
    campoPesquisa.addEventListener('input', function () {
      const termo = this.value.toLowerCase();
      const linhas = document.querySelectorAll('table tbody tr');

      linhas.forEach(linha => {
        const textoLinha = linha.textContent.toLowerCase();
        linha.style.display = textoLinha.includes(termo) ? '' : 'none';
      });
    });
  }
});
