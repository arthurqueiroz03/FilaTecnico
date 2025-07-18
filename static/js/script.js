const form = document.getElementById('form-agendamento');
  const msgSucesso = document.getElementById('msg-sucesso');
  const botaoOk = document.getElementById('ok');

  form.addEventListener('submit', function(event) {
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
  botaoOk.addEventListener('click', function() {
    msgSucesso.style.display = 'none';
  });