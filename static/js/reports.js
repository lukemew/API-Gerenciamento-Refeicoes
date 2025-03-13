// Função para buscar o relatório de calorias por usuário
async function fetchReport(event) {
  event.preventDefault();

  const userId = document.getElementById("user-id").value;

  const response = await fetch(`/api/reports/user/${userId}/calories`);
  const data = await response.json();

  const reportMessage = document.getElementById("report-message");
  const reportDetails = document.getElementById("report-details");

  // Limpa o conteúdo anterior
  reportMessage.textContent = "";
  reportDetails.innerHTML = "";

  if (response.ok) {
    // Exibe o relatório
    reportMessage.textContent = data.message;

    // Adiciona detalhes do relatório
    const li = document.createElement("li");
    li.textContent = `Total de Calorias: ${data.total_calories}`;
    reportDetails.appendChild(li);
  } else {
    // Exibe mensagem de erro
    reportMessage.textContent = data.detail || "Erro ao buscar relatório";
  }
}

// Adiciona um listener para o formulário de busca de relatório
document.getElementById("report-form").addEventListener("submit", fetchReport);
