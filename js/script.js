const form = document.getElementById("form-agendamento");

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const data = form.data.value;
            const hora = form.hora.value;
            const descricao = form.descricao.value;

            await fetch("/agendar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ data, hora, descricao })
            });

            form.reset();
            carregarAgenda(); // Atualiza a tabela após enviar
        });

        async function carregarAgenda() {
            const resposta = await fetch("/agenda");
            const agenda = await resposta.json();

            const tabela = document.getElementById("tabela-agenda");
            tabela.innerHTML = "";

            agenda.forEach(item => {
                const linha = `
                    <tr>
                        <td>${item.data}</td>
                        <td>${item.hora}</td>
                        <td>${item.descricao}</td>
                    </tr>
                `;
                tabela.innerHTML += linha;
            });
        }

        // Atualiza a tabela ao carregar a página
        carregarAgenda();

        // Atualiza a cada 10 segundos (quase em tempo real)
        setInterval(carregarAgenda, 10000);