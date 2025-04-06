document.addEventListener("DOMContentLoaded", () => {
  loadUsers();
});

document
  .getElementById("add-user-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;

    const response = await fetch("/api/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age, gender }),
    });

    if (response.ok) {
      loadUsers();
      document.getElementById("add-user-form").reset();
    } else {
      alert("Erro ao adicionar usuário.");
    }
  });

async function loadUsers() {
  try {
    const response = await fetch("/api/users/");
    if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);

    const { data: users } = await response.json();
    const userList = document.getElementById("users");
    userList.innerHTML = ""; // Limpa a lista antes de adicionar os novos elementos

    users.forEach((user) => {
      const li = document.createElement("li");
      li.innerHTML = `ID: ${user.id}, Nome: ${user.name}, Idade: ${user.age}, Gênero: ${user.gender} `;

      // Criando Botão de Editar
      const editButton = document.createElement("button");
      editButton.textContent = "✏️";
      editButton.classList.add("edit-user");
      editButton.dataset.id = user.id;
      editButton.dataset.name = user.name;
      editButton.dataset.age = user.age;
      editButton.dataset.gender = user.gender;
      editButton.addEventListener("click", function () {
        editUser(user.id, user.name, user.age, user.gender);
      });

      // Criando Botão de Remover
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "🗑";
      deleteButton.classList.add("delete-user");
      deleteButton.dataset.id = user.id;
      deleteButton.addEventListener("click", function () {
        deleteUser(user.id);
      });

      li.appendChild(editButton);
      li.appendChild(deleteButton);
      userList.appendChild(li);
    });
  } catch (error) {
    console.error("Erro ao carregar usuários:", error);
  }
}

async function editUser(userId, currentName, currentAge, currentGender) {
  const newName = prompt("Novo nome:", currentName);
  const newAge = prompt("Nova idade:", currentAge);
  const newGender = prompt("Novo gênero:", currentGender);

  if (!newName && !newAge && !newGender) {
    alert("Nenhum campo foi modificado!");
    return;
  }

  const updatedData = {};
  if (newName) updatedData.name = newName;
  if (newAge) updatedData.age = parseInt(newAge);
  if (newGender) updatedData.gender = newGender;

  try {
    const response = await fetch(`/api/users/${userId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedData),
    });

    if (response.ok) {
      loadUsers();
    } else {
      alert("Erro ao editar usuário.");
    }
  } catch (error) {
    console.error("Erro ao editar usuário:", error);
  }
}

async function deleteUser(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`, { method: "DELETE" });
    if (response.ok) {
      loadUsers();
    } else {
      alert("Erro ao remover usuário.");
    }
  } catch (error) {
    console.error("Erro ao remover usuário:", error);
  }
}
