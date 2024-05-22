function toggleDarkmode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
  }

  const darkModeToggle = document.getElementById('DarkModeToggle');
  darkModeToggle.addEventListener('click', toggleDarkmode);
