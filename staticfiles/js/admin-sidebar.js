document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll("#nav-sidebar-apps .module").forEach(app => {

        const title = app.querySelector("h2");

        if (!title) return;

        const menu = app.querySelector("ol.flex");

        if (!menu) return;

        if (!app.classList.contains("current-app")) {
            menu.style.display = "none";
        }

        title.style.cursor = "pointer";

        title.addEventListener("click", (e) => {

            e.preventDefault();

            if (menu.style.display === "none") {
                menu.style.display = "flex";
            } else {
                menu.style.display = "none";
            }

        });

    });

});
