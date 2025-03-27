document.addEventListener("DOMContentLoaded", function () {
  const userSelect = document.getElementById("user-select");
  const activitiesList = document.getElementById("activities");
  const API_BASE_URL = "/api/activities"; // URL base definida aqui

  // Carrega os usuários no select
  function loadUsers() {
    fetch("/api/users")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const users = data.data;
        userSelect.innerHTML = '<option value="">Escolha um usuário</option>';
        users.forEach((user) => {
          const option = document.createElement("option");
          option.value = user.id;
          option.textContent = `Usuário ID: ${user.id} - ${user.name}`;
          userSelect.appendChild(option);
        });
      })
      .catch((error) => {
        console.error("Erro ao carregar usuários:", error);
        alert("Erro ao carregar lista de usuários");
      });
  }

  // Carrega as atividades do usuário selecionado
  async function loadActivities(userId) {
    try {
      const response = await fetch(`/api/activities?user_id=${userId}`);
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Erro ao carregar atividades");
      }
      const data = await response.json();

      activitiesList.innerHTML = "";

      if (data.length === 0) {
        activitiesList.innerHTML =
          "<li>Nenhuma atividade encontrada para este usuário.</li>";
        return;
      }

      data.forEach((activity) => {
        const li = document.createElement("li");
        li.innerHTML = `
          ${activity.activity} (${activity.intensity}) - 
          ${activity.duration} min - 
          ${Math.round(activity.calories_burned)} kcal -
          ${new Date(activity.date).toLocaleDateString()}
          <button class="edit-activity" data-id="${
            activity.id
          }">✏️ Editar</button>
          <button class="delete-activity" data-id="${
            activity.id
          }">🗑 Remover</button>
        `;
        activitiesList.appendChild(li);
      });

      // Adiciona eventos aos botões de edição
      document.querySelectorAll(".edit-activity").forEach((button) => {
        button.addEventListener("click", function () {
          const activityId = this.getAttribute("data-id");
          editActivity(activityId, userId);
        });
      });

      // Adiciona eventos aos botões de exclusão
      document.querySelectorAll(".delete-activity").forEach((button) => {
        button.addEventListener("click", function () {
          const activityId = this.getAttribute("data-id");
          deleteActivity(activityId, userId);
        });
      });
    } catch (error) {
      console.error("Erro ao carregar atividades:", error);
      alert(error.message);
    }
  }

  // Exclui uma atividade
  function deleteActivity(activityId, userId) {
    fetch(`${API_BASE_URL}/${activityId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(() => loadActivities(userId))
      .catch((error) => {
        console.error("Erro ao excluir atividade:", error);
        alert("Erro ao excluir atividade");
      });
  }

  // Edita uma atividade
  function editActivity(activityId, userId) {
    const activity = prompt("Nova atividade (Bike, Caminhada, etc.):");
    const intensity = prompt("Nova intensidade (baixa, média, alta):");
    const duration = prompt("Nova duração (minutos):");

    if (!activity || !intensity || !duration) {
      alert("Todos os campos são obrigatórios!");
      return;
    }

    const activityData = {
      activity,
      intensity,
      duration: parseInt(duration),
    };

    fetch(`${API_BASE_URL}/${activityId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(activityData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(() => loadActivities(userId))
      .catch((error) => {
        console.error("Erro ao editar atividade:", error);
        alert(error.message);
      });
  }

  // Adiciona uma nova atividade
  document
    .getElementById("add-activity-form")
    .addEventListener("submit", async function (e) {
      e.preventDefault();

      try {
        const userId = document.getElementById("user-id").value;
        const activity = document.getElementById("activity").value;
        const intensity = document.getElementById("intensity").value;
        const duration = document.getElementById("duration").value;

        // Validação básica
        if (!userId || !activity || !intensity || !duration) {
          throw new Error("Todos os campos são obrigatórios!");
        }

        const response = await fetch("/api/activities", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: parseInt(userId),
            activity,
            intensity,
            duration: parseInt(duration),
          }),
        });

        // Verifica se a resposta é JSON antes de tentar parsear
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          const text = await response.text();
          throw new Error(text || "Resposta inválida do servidor");
        }

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Erro ao registrar atividade");
        }

        // Limpa o formulário
        e.target.reset();

        // Recarrega atividades se o usuário estiver selecionado
        const selectedUserId = userSelect.value;
        if (selectedUserId) {
          loadActivities(selectedUserId);
        }

        alert("Atividade registrada com sucesso!");
      } catch (error) {
        console.error("Erro detalhado:", error);
        alert(`Erro: ${error.message}`);
      }
    });

  // Atualiza a lista quando o usuário é selecionado
  userSelect.addEventListener("change", function () {
    const userId = this.value;
    if (userId) {
      loadActivities(userId);
    } else {
      activitiesList.innerHTML = "";
    }
  });

  // Carrega os usuários ao iniciar
  loadUsers();
});
