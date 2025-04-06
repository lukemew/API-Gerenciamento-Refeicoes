document.addEventListener("DOMContentLoaded", function () {
  const userSelect = document.getElementById("user-select");
  const mealsList = document.getElementById("meals");
  const addMealForm = document.getElementById("add-meal-form");
  const API_BASE_URL = "/api/meals";

  function loadUsers() {
    fetch("/api/users")
      .then((response) => response.json())
      .then((data) => {
        userSelect.innerHTML = '<option value="">Escolha um usuário</option>';
        data.data.forEach((user) => {
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

  async function loadMeals(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/?user_id=${userId}`);

      if (!response.ok) throw new Error(await response.text());

      const meals = await response.json();
      mealsList.innerHTML = meals.length
        ? meals
            .map(
              (meal) => `
          <li>
            <strong>${meal.meal_type}</strong> - ${meal.calories} kcal (${meal.date})
            <br>Itens: ${meal.food_items}
            <div class="button-container">
            <button class="edit-meal" data-id="${meal.id}">✏️</button>
            <button class="delete-meal" data-id="${meal.id}">🗑</button>
            </div>
          </li>`
            )
            .join("")
        : "<li>Nenhuma refeição encontrada.</li>";

      document.querySelectorAll(".edit-meal").forEach((btn) => {
        btn.addEventListener("click", () => editMeal(btn.dataset.id, userId));
      });

      document.querySelectorAll(".delete-meal").forEach((btn) => {
        btn.addEventListener("click", () => deleteMeal(btn.dataset.id, userId));
      });
    } catch (error) {
      console.error("Erro ao carregar refeições:", error);
      alert("Erro ao carregar refeições");
    }
  }

  async function deleteMeal(mealId, userId) {
    if (!confirm("Tem certeza que deseja excluir esta refeição?")) return;

    try {
      const response = await fetch(`${API_BASE_URL}/${mealId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error((await response.json()).detail);

      await loadMeals(userId);
      alert("Refeição excluída com sucesso!");
    } catch (error) {
      console.error("Erro:", error);
      alert(error.message);
    }
  }

  function editMeal(mealId) {
    console.log("mealId recebido:", mealId); // Verificar se mealId está correto

    if (!mealId) {
      alert("Erro: ID da refeição não encontrado!");
      return;
    }

    // Primeiro, busca os dados da refeição antes de editar
    fetch(`/api/meals/${mealId}`)
      .then((response) => {
        if (!response.ok) throw new Error("Erro ao buscar dados da refeição");
        return response.json();
      })
      .then((currentMeal) => {
        console.log("Dados da refeição:", currentMeal);

        // Pede os novos valores ao usuário
        const meal_type = prompt("Tipo de refeição:", currentMeal.meal_type);
        const food_items = prompt(
          "Itens alimentares (separados por vírgula):",
          currentMeal.food_items
        );
        const calories = prompt("Calorias:", currentMeal.calories);
        const date = prompt("Data (YYYY-MM-DD):", currentMeal.date);

        if (!meal_type || !food_items || !calories || !date) {
          alert("Todos os campos são obrigatórios!");
          return;
        }

        const mealData = {
          meal_type,
          food_items,
          calories: parseInt(calories),
          date,
        };

        return fetch(`/api/meals/${mealId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(mealData),
        });
      })
      .then((response) => {
        if (!response.ok) throw new Error("Erro ao atualizar refeição");
        alert("Refeição atualizada com sucesso!");
        location.reload(); // Recarrega a página para mostrar os dados atualizados
      })
      .catch((error) => {
        console.error("Erro ao editar refeição:", error);
        alert(error.message);
      });
  }

  addMealForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    try {
      const userId = userSelect.value;
      if (!userId) throw new Error("Selecione um usuário!");

      const mealType = document.getElementById("meal-type").value;
      const foodItems = document.getElementById("food-items").value;
      const calories = document.getElementById("calories").value;
      const date = document.getElementById("date").value;

      if (!mealType || !foodItems || !calories || !date)
        throw new Error("Todos os campos são obrigatórios!");

      const response = await fetch(API_BASE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: parseInt(userId),
          meal_type: mealType,
          food_items: foodItems.split(",").map((item) => item.trim()),
          calories: parseInt(calories),
          date,
        }),
      });

      if (!response.ok)
        throw new Error(
          (await response.json()).detail || "Erro ao adicionar refeição"
        );

      addMealForm.reset();
      loadMeals(userId);
      alert("Refeição adicionada com sucesso!");
    } catch (error) {
      console.error("Erro ao adicionar refeição:", error);
      alert(`Erro: ${error.message}`);
    }
  });

  userSelect.addEventListener("change", function () {
    this.value ? loadMeals(this.value) : (mealsList.innerHTML = "");
  });

  loadUsers();
});
