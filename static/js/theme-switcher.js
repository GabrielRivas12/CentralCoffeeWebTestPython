document.addEventListener('DOMContentLoaded', () => {
    const themeSwitches = document.querySelectorAll('.theme-switch');
    const body = document.body;

    // Función para aplicar el tema claro
    function setTheme(isLight) {
        if (isLight) {
            body.classList.add('light-theme');
            localStorage.setItem('sidebarTheme', 'light');
            themeSwitches.forEach(sw => sw.checked = true);
        } else {
            body.classList.remove('light-theme');
            localStorage.setItem('sidebarTheme', 'dark'); // El default es 'dark'
            themeSwitches.forEach(sw => sw.checked = false);
        }
    }

    // Añadir un listener a cada checkbox
    themeSwitches.forEach(sw => {
        sw.addEventListener('change', (e) => {
            setTheme(e.target.checked);
        });
    });

    // Al cargar la página, aplicar el tema guardado
    const savedTheme = localStorage.getItem('sidebarTheme');
    if (savedTheme === 'light') {
        setTheme(true);
    } else {
        setTheme(false); // Por defecto, el tema oscuro (sin la clase)
    }
});
