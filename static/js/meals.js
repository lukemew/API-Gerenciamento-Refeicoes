document.addEventListener("DOMContentLoaded", () => {
  loadMeals(); // Carregar refeições ao carregar a página
});

document
  .getElementById("add-meal-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const userId = parseInt(document.getElementById("user-id").value, 10);
    if (isNaN(userId) || userId <= 0) {
      alert("Por favor, insira um ID de usuário válido.");
      return;
    }

    const mealType = document.getElementById("meal-type").value;
    const foodItems = document.getElementById("food-items").value.split(",");
    const calories = parseInt(document.getElementById("calories").value, 10);
    const date = document.getElementById("date").value;

    const response = await fetch("/api/meals/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        meal_type: mealType,
        food_items: foodItems,
        calories: calories,
        date: date,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert(errorData.detail);
    } else {
      alert("Refeição adicionada com sucesso!");
      loadMeals(); // Atualiza a lista de refeições automaticamente
    }
  });

// Função para carregar as refeições e exibi-las na página
async function loadMeals() {
  try {
    const response = await fetch("/api/meals/");
    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.status}`);
    }

    const responseData = await response.json();
    const meals = responseData.data; // Ajustando para acessar a lista dentro de "data"

    const mealsList = document.getElementById("meals");
    mealsList.innerHTML = ""; // Limpa a lista antes de adicionar novas refeições

    meals.forEach((meal) => {
      const listItem = document.createElement("li");
      listItem.textContent = `${meal.meal_type} - ${meal.food_items} - ${meal.calories} kcal (${meal.date})`;
      mealsList.appendChild(listItem);
    });
  } catch (error) {
    console.error("Erro ao carregar refeições:", error);
  }
}
