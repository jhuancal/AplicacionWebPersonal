document.addEventListener('DOMContentLoaded', function () {
    updateHUD();
});

function updateHUD() {
    fetch('/api/user/hud')
        .then(response => response.json())
        .then(data => {
            if (data) {
                // Update specific HUD elements if they have IDs
                // Note: The current template renders partials from the backend, 
                // so we might just use this for live updates later.
                // For now, let's log it to confirm connection.
                console.log("HUD Data Loaded:", data);

                // Example of updating elements if we add IDs to game_base.html
                /*
                document.getElementById('hud-username').textContent = data.username;
                document.getElementById('hud-rank').textContent = data.rank;
                document.getElementById('hud-points').textContent = data.points;
                */
            }
        })
        .catch(error => console.error('Error fetching HUD data:', error));
}
