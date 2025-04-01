document.addEventListener("DOMContentLoaded", function () {
  const userSelect = document.getElementById("user-select");
  const activitiesList = document.getElementById("activities");
  const addActivityForm = document.getElementById("add-activity-form");
  const API_BASE_URL = "/api/activities";

  function loadUsers() {
    fetch("/api/users")
      .then((response) => response.json())
      .then((data) => {
        const users = data.data;
        userSelect.innerHTML = '<option value="">Escolha um usuário</option>';
        users.forEach((user) => {
          const option = document.createElement("option");
          option.value = user.id;
          option.textContent = `${user.name} (ID: ${user.id})`;
          userSelect.appendChild(option);
        });
      })
      .catch((error) => {
        console.error("Erro ao carregar usuários:", error);
        alert("Erro ao carregar lista de usuários");
      });
  }

  async function loadActivities(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}?user_id=${userId}`);
      if (!response.ok) throw new Error(await response.text());

      const data = await response.json();
      activitiesList.innerHTML = "";

      if (data.length === 0) {
        activitiesList.innerHTML = "<li>Nenhuma atividade encontrada.</li>";
        return;
      }

      data.forEach((activity) => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${activity.activity}</strong> (${activity.intensity}) - 
          ${activity.duration} min, ${Math.round(activity.calories_burned)} kcal
          <button class="edit-activity" data-id="${activity.id}">✏️</button>
          <button class="delete-activity" data-id="${activity.id}">🗑</button>
        `;
        activitiesList.appendChild(li);
      });

      // Adiciona eventos aos botões
      document.querySelectorAll(".edit-activity").forEach((btn) => {
        btn.addEventListener("click", () =>
          editActivity(btn.dataset.id, userId)
        );
      });

      document.querySelectorAll(".delete-activity").forEach((btn) => {
        btn.addEventListener("click", () =>
          deleteActivity(btn.dataset.id, userId)
        );
      });
    } catch (error) {
      console.error("Erro ao carregar atividades:", error);
      alert("Erro ao carregar atividades");
    }
  }

  function deleteActivity(activityId, userId) {
    if (!confirm("Tem certeza que deseja excluir esta atividade?")) return;

    fetch(`${API_BASE_URL}/${activityId}`, { method: "DELETE" })
      .then(() => loadActivities(userId))
      .catch((error) => {
        console.error("Erro ao excluir atividade:", error);
        alert("Erro ao excluir atividade");
      });
  }

  function editActivity(activityId, userId) {
    // Primeiro busca os dados atuais da atividade
    fetch(`${API_BASE_URL}/${activityId}`)
      .then((response) => response.json())
      .then((currentActivity) => {
        // Preenche os prompts com valores atuais
        const activity = prompt("Atividade:", currentActivity.activity);
        const intensity = prompt(
          "Intensidade (baixa, média, alta):",
          currentActivity.intensity
        );
        const duration = prompt("Duração (minutos):", currentActivity.duration);

        if (!activity || !intensity || !duration) {
          alert("Todos os campos são obrigatórios!");
          return;
        }

        const activityData = {
          activity,
          intensity,
          duration: parseInt(duration),
        };

        return fetch(`${API_BASE_URL}/${activityId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(activityData),
        });
      })
      .then((response) => {
        if (!response.ok) throw new Error("Erro ao atualizar atividade");
        loadActivities(userId);
        alert("Atividade atualizada com sucesso!");
      })
      .catch((error) => {
        console.error("Erro ao editar atividade:", error);
        alert(error.message);
      });
  }

  addActivityForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    try {
      const userId = userSelect.value; // Já pega do select
      const activity = document.getElementById("activity").value;
      const intensity = document.getElementById("intensity").value;
      const duration = document.getElementById("duration").value;

      if (!userId || !activity || !intensity || !duration) {
        throw new Error("Todos os campos são obrigatórios!");
      }

      const response = await fetch(API_BASE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: parseInt(userId), // Conversão para número
          activity,
          intensity,
          duration: parseInt(duration), // Conversão para número
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Erro ao registrar atividade");
      }

      addActivityForm.reset();
      loadActivities(userId);
      alert("Atividade registrada com sucesso!");
    } catch (error) {
      console.error("Erro detalhado:", error);
      alert(`Erro: ${error.message}`);
    }
  });

  userSelect.addEventListener("change", function () {
    if (this.value) loadActivities(this.value);
    else activitiesList.innerHTML = "";
  });

  loadUsers();
});
