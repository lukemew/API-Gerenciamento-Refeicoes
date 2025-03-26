document.addEventListener("DOMContentLoaded", function () {
  const userSelect = document.getElementById("user-select");
  const mealsList = document.getElementById("meals");

  function loadUsers() {
    fetch("/api/users")
      .then((response) => response.json())
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
      .catch((error) => console.error("Erro ao carregar usuários:", error));
  }

  function loadMeals(userId) {
    fetch(`/api/meals?user_id=${userId}`)
      .then((response) => response.json())
      .then((data) => {
        const meals = data.data;
        mealsList.innerHTML = "";

        if (meals.length === 0) {
          mealsList.innerHTML =
            "<li>Nenhuma refeição encontrada para este usuário.</li>";
          return;
        }

        meals.forEach((meal) => {
          const li = document.createElement("li");
          li.innerHTML = `${meal.meal_type} - ${meal.calories} kcal - ${meal.date}
            <button class="edit-meal" data-id="${meal.id}">✏️ Editar</button>
            <button class="delete-meal" data-id="${meal.id}">🗑 Remover</button>`;

          mealsList.appendChild(li);
        });

        document.querySelectorAll(".edit-meal").forEach((button) => {
          button.addEventListener("click", function () {
            const mealId = this.getAttribute("data-id");
            editMeal(mealId, userId);
          });
        });

        document.querySelectorAll(".delete-meal").forEach((button) => {
          button.addEventListener("click", function () {
            const mealId = this.getAttribute("data-id");
            deleteMeal(mealId, userId);
          });
        });
      })
      .catch((error) => console.error("Erro ao carregar refeições:", error));
  }

  function deleteMeal(mealId, userId) {
    fetch(`/api/meals/${mealId}`, { method: "DELETE" })
      .then(() => loadMeals(userId))
      .catch((error) => console.error("Erro ao excluir refeição:", error));
  }

  function editMeal(mealId, userId) {
    const mealType = prompt(
      "Novo tipo de refeição (ex: Café da manhã, Almoço):"
    );
    const foodItems = prompt("Alimentos (separados por vírgula):");
    const calories = prompt("Nova quantidade de calorias:");
    const date = prompt("Nova data (YYYY-MM-DD):");

    if (!mealType || !foodItems || !calories || !date) {
      alert("Todos os campos são obrigatórios!");
      return;
    }

    const mealData = {
      meal_type: mealType,
      food_items: foodItems.split(",").map((item) => item.trim()), // Converte string em lista
      calories: parseInt(calories), // Garante que é número
      date: date,
    };

    fetch(`/api/meals/${mealId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(mealData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao atualizar refeição!");
        }
        return response.json();
      })
      .then(() => loadMeals(userId))
      .catch((error) => console.error("Erro ao editar refeição:", error));
  }

  userSelect.addEventListener("change", function () {
    const userId = userSelect.value;
    if (userId) {
      loadMeals(userId);
    } else {
      mealsList.innerHTML = "";
    }
  });

  loadUsers();
});
