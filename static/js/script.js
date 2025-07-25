document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('form-agendamento');
  const msgSucesso = document.getElementById('msg-sucesso');
  const botaoOk = document.getElementById('ok');
  const okok = document.getElementById('fechar');

  // Apagar agendamento ao clicar na linha da tabela
  document.querySelectorAll('.btn-apagar').forEach(btn => {
    btn.addEventListener('click', function (event) {
      event.stopPropagation();
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

  //Editar diretamente na linha
document.querySelectorAll('.editavel').forEach(cell => {
    cell.addEventListener('blur', function () {
        const id = this.dataset.id;
        const campo = this.dataset.campo;
        const valor = this.textContent.trim();

        fetch(`/editar/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ campo, valor })
        })
        .then(res => {
            if (!res.ok) throw new Error("Erro ao salvar");
        })
        .catch(err => {
            alert("Erro ao salvar alteração.");
            console.error(err);
        });
    });
});

// histórico 
document.querySelectorAll('.historico').forEach(btn => {
    btn.addEventListener('click', function (event) {
        event.stopPropagation();

        const id = this.dataset.id;
        if (!id) return;

        fetch(`/agendamento_info/${id}`)
            .then(res => res.json())
            .then(data => {
                const popup = document.getElementById('caixahistorico');

                document.getElementById('info-criado').textContent = `Feito por: ${data.criado_por || 'N/A'}`;
                document.getElementById('info-alterado').textContent = `Alterado por: ${data.alterado_por || 'N/A'}`;
                document.getElementById('info-alterado-em').textContent = `Em: ${data.alterado_em || 'N/A'}`;

                // Posiciona o popup próximo ao botão clicado
                const rect = btn.getBoundingClientRect();
                popup.style.top = `${rect.bottom + window.scrollY + 5}px`; // 5px abaixo do botão
                popup.style.left = `${rect.left + window.scrollX -200}px`;
                popup.style.display = 'block';
            })
            .catch(err => {
                alert("Erro ao buscar informações do agendamento.");
                console.error(err);
            });
    });
});

if (fechar) {
    fechar.addEventListener('click', function() {
      caixahistorico.style.display = 'none';
    });
  }

  // Submissão do formulário
  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault();
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
