// Função para buscar o relatório de calorias por usuário
async function fetchReport(event) {
  event.preventDefault();

  const userId = document.getElementById("user-id").value;

  try {
    const response = await fetch(`/api/reports/user/${userId}/calories`);
    const data = await response.json();

    const reportMessage = document.getElementById("report-message");
    const reportDetails = document.getElementById("report-details");

    // Limpa o conteúdo anterior
    reportMessage.textContent = "";
    reportDetails.innerHTML = "";

    if (response.ok) {
      // Exibe o relatório principal
      reportMessage.textContent = data.message;

      // Adiciona detalhes do relatório
      const li1 = document.createElement("li");
      li1.textContent = `Calorias Consumidas: ${data.total_calories_consumed}`;
      reportDetails.appendChild(li1);

      const li2 = document.createElement("li");
      li2.textContent = `Calorias Gastas: ${data.total_calories_burned}`;
      reportDetails.appendChild(li2);

      const li3 = document.createElement("li");
      li3.textContent = `Balanço Final: ${data.balance}`;
      reportDetails.appendChild(li3);
    } else {
      // Exibe mensagem de erro
      reportMessage.textContent = data.detail || "Erro ao buscar relatório";
    }
  } catch (error) {
    console.error("Erro ao buscar relatório:", error);
    document.getElementById("report-message").textContent =
      "Erro ao buscar relatório.";
  }
}

// Adiciona um listener para o formulário de busca de relatório
document.getElementById("report-form").addEventListener("submit", fetchReport);
