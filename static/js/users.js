// Função para carregar a lista de usuários
async function loadUsers() {
  try {
    const response = await fetch("/api/users");
    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.status}`);
    }
    const data = await response.json();
    console.log("Dados recebidos:", data); // Depuração
    const userList = document.getElementById("users");

    // Limpa a lista atual
    userList.innerHTML = "";

    // Adiciona cada usuário à lista
    data.data.forEach((user) => {
      const li = document.createElement("li");
      li.textContent = `ID: ${user.id}, Nome: ${user.name}, Idade: ${user.age}, Gênero: ${user.gender}`;
      userList.appendChild(li);
    });
  } catch (error) {
    console.error("Erro ao carregar usuários:", error);
  }
}

// Função para adicionar um novo usuário
async function addUser(event) {
  event.preventDefault();

  const name = document.getElementById("name").value;
  const age = document.getElementById("age").value;
  const gender = document.getElementById("gender").value;

  const response = await fetch("/add-user", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `name=${encodeURIComponent(name)}&age=${encodeURIComponent(
      age
    )}&gender=${encodeURIComponent(gender)}`,
  });

  if (response.ok) {
    // Recarrega a lista de usuários após adicionar um novo
    loadUsers();
    // Limpa o formulário
    document.getElementById("add-user-form").reset();
  } else {
    alert("Erro ao adicionar usuário");
  }
}

// Carrega a lista de usuários ao carregar a página
document.addEventListener("DOMContentLoaded", loadUsers);

// Adiciona um listener para o formulário de adicionar usuário
document.getElementById("add-user-form").addEventListener("submit", addUser);
