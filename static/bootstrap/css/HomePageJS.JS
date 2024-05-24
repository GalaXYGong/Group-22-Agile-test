function toggleDarkmode() {
  var element = document.body;
  element.classList.toggle("dark-mode");

  var darkMode = element.classList.contains("dark-mode");
  localStorage.setItem('darkMode', darkMode);

  var button = document.getElementById('DarkModeToggle');
  button.textContent = darkMode ? 'Light' : 'Dark';
}

window.onload = function() {
  var darkMode = localStorage.getItem('darkMode') === 'true';
  document.body.classList.toggle("dark-mode", darkMode);

  var button = document.getElementById('DarkModeToggle');
  button.textContent = darkMode ? 'Light' : 'Dark';
}

const darkModeToggle = document.getElementById('DarkModeToggle');
darkModeToggle.addEventListener('click', toggleDarkmode);