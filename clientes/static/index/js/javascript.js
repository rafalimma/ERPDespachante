function Cliquefora(event) {
    const sidebar = document.getElementById("mySidebar");
    const toggle = document.querySelector(".menu-toggle");

    // Garante que clique no botão do menu não feche a sidebar
    // se o elemento clicado não estiver dentro da side bar feche a side bar
    if (!sidebar.contains(event.target) && !toggle.contains(event.target)) {
        sidebar.classList.remove("active");
        document.removeEventListener("click", Cliquefora);
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById("mySidebar");

    sidebar.classList.toggle("active");

    if (sidebar.classList.contains("active")) {
        document.addEventListener("click", Cliquefora);
    } else {
        document.removeEventListener("click", Cliquefora);
    }
}