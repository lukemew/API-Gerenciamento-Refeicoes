document.addEventListener("DOMContentLoaded", function () {
  const userSelect = document.getElementById("user-select");
  const mealsList = document.getElementById("meals");
  const addMealForm = document.getElementById("add-meal-form");
  const API_BASE_URL = "/api/meals";

  async function loadUsers() {
    try {
      const response = await fetch("/api/users");
      if (!response.ok) throw new Error(await response.text());

      const { data: users } = await response.json();
      userSelect.innerHTML = '<option value="">Selecione um usuário</option>';

      users.forEach((user) => {
        const option = document.createElement("option");
        option.value = user.id;
        option.textContent = `${user.name} (ID: ${user.id})`;
        userSelect.appendChild(option);
      });
    } catch (error) {
      console.error("Erro:", error);
      alert(error.message);
    }
  }

  async function loadMeals(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}?user_id=${userId}`);

      if (response.status === 404) {
        mealsList.innerHTML = "<li>Usuário não encontrado</li>";
        return;
      }

      if (!response.ok) throw new Error(await response.text());

      const meals = await response.json();
      mealsList.innerHTML = "";

      if (meals.length === 0) {
        mealsList.innerHTML =
          "<li>Nenhuma refeição encontrada para este usuário.</li>";
        return;
      }

      meals.forEach((meal) => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${meal.meal_type}</strong> - ${meal.calories} kcal (${meal.date})
          <br>Itens: ${meal.food_items}
          <button class="edit-meal" data-id="${meal.id}">✏️</button>
          <button class="delete-meal" data-id="${meal.id}">🗑</button>
        `;
        mealsList.appendChild(li);
      });

      // Adiciona eventos aos botões
      document.querySelectorAll(".edit-meal").forEach((btn) => {
        btn.addEventListener("click", () => editMeal(btn.dataset.id, userId));
      });

      document.querySelectorAll(".delete-meal").forEach((btn) => {
        btn.addEventListener("click", () => deleteMeal(btn.dataset.id, userId));
      });
    } catch (error) {
      console.error("Erro ao carregar refeições:", error);
      alert("Erro ao carregar refeições do usuário");
    }
  }

  // Deleta uma refeição
  async function deleteMeal(mealId, userId) {
    if (!confirm("Tem certeza que deseja excluir esta refeição?")) return;

    try {
      const response = await fetch(`${API_BASE_URL}/${mealId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error(await response.text());

      loadMeals(userId);
    } catch (error) {
      console.error("Erro ao excluir refeição:", error);
      alert("Erro ao excluir refeição");
    }
  }

  // Edita uma refeição
  async function editMeal(mealId, userId) {
    try {
      // Busca os dados atuais da refeição
      const response = await fetch(`${API_BASE_URL}/${mealId}`);
      if (!response.ok) throw new Error(await response.text());

      const currentMeal = await response.json();

      // Preenche os prompts com valores atuais
      const mealType = prompt("Tipo de refeição:", currentMeal.meal_type);
      const foodItems = prompt(
        "Alimentos (separados por vírgula):",
        currentMeal.food_items
      );
      const calories = prompt("Calorias:", currentMeal.calories);
      const date = prompt("Data (YYYY-MM-DD):", currentMeal.date);

      if (!mealType || !foodItems || !calories || !date) {
        alert("Todos os campos são obrigatórios!");
        return;
      }

      const mealData = {
        meal_type: mealType,
        food_items: foodItems.split(",").map((item) => item.trim()),
        calories: parseInt(calories),
        date: date,
      };

      const updateResponse = await fetch(`${API_BASE_URL}/${mealId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(mealData),
      });

      if (!updateResponse.ok) throw new Error("Erro ao atualizar refeição");

      loadMeals(userId);
      alert("Refeição atualizada com sucesso!");
    } catch (error) {
      console.error("Erro ao editar refeição:", error);
      alert(error.message);
    }
  }

  // Adiciona uma nova refeição
  addMealForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    try {
      const userId = userSelect.value;
      const mealType = document.getElementById("meal-type").value;
      const foodItems = document.getElementById("food-items").value;
      const calories = document.getElementById("calories").value;
      const date = document.getElementById("date").value;

      if (!userId || !mealType || !foodItems || !calories || !date) {
        throw new Error("Todos os campos são obrigatórios!");
      }

      const response = await fetch(API_BASE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: parseInt(userId),
          meal_type: mealType,
          food_items: foodItems.split(",").map((item) => item.trim()),
          calories: parseInt(calories),
          date: date,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Erro ao adicionar refeição");
      }

      // Limpa o formulário e recarrega as refeições
      addMealForm.reset();
      await loadMeals(userId);
      alert("Refeição adicionada com sucesso!");
    } catch (error) {
      console.error("Erro detalhado:", error);
      alert(`Erro: ${error.message}`);
    }
  });

  userSelect.addEventListener("change", function () {
    if (this.value) {
      loadMeals(this.value);
    } else {
      mealsList.innerHTML = "";
    }
  });

  loadUsers();
});
