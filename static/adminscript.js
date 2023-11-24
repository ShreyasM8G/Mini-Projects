document.addEventListener("DOMContentLoaded", function () {
    // Function to open a dialog by its ID
    function openDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        dialog.style.display = "block";
    }

    // Function to close a dialog by its ID
    function closeDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        dialog.style.display = "none";
    }

    // Function to handle form submissions
    function handleSubmit(event, route) {
        event.preventDefault();

        const form = new FormData(event.target);

        fetch(route, {
            method: "POST",
            body: form
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            closeDialog(`${event.target.id}-dialog`);
        })
        .catch(error => console.error("Error:", error));
    }

    // Add event listeners for opening dialog boxes
    document.getElementById("create-match").addEventListener("click", () => openDialog("create-match-dialog"));
    document.getElementById("create-tournament").addEventListener("click", () => openDialog("create-tournament-dialog"));
    document.getElementById("create-team").addEventListener("click", () => openDialog("create-team-dialog"));
    document.getElementById("create-game").addEventListener("click", () => openDialog("create-game-dialog"));
    document.getElementById("add-developer").addEventListener("click", () => openDialog("game-developer-dialog"));

    // Add event listeners for closing dialog boxes
    document.getElementById("cancel-match").addEventListener("click", () => closeDialog("create-match-dialog"));
    document.getElementById("cancel-tournament").addEventListener("click", () => closeDialog("create-tournament-dialog"));
    document.getElementById("cancel-team").addEventListener("click", () => closeDialog("create-team-dialog"));
    document.getElementById("cancel-game").addEventListener("click", () => closeDialog("create-game-dialog"));
    document.getElementById("cancel-developer").addEventListener("click", () => closeDialog("game-developer-dialog"));

    // Add event listeners for form submissions
    document.getElementById("create-match-dialog").addEventListener("submit", (event) => handleSubmit(event, "/create_match"));
    document.getElementById("create-tournament-dialog").addEventListener("submit", (event) => handleSubmit(event, "/create_tournament"));
    document.getElementById("create-team-dialog").addEventListener("submit", (event) => handleSubmit(event, "/create_team"));
    document.getElementById("create-game-dialog").addEventListener("submit", (event) => handleSubmit(event, "/create_game"));
    document.getElementById("game-developer-dialog").addEventListener("submit", (event) => handleSubmit(event, "/add_developer"));
});
