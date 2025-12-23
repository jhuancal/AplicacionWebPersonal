document.addEventListener('DOMContentLoaded', function () {
    loadDashboardStats();
    loadDailyChallenge();
    loadCourseProgress();
});

function loadDashboardStats() {
    fetch('/api/dashboard/stats')
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('stat-rank').textContent = data.rank;
                document.getElementById('stat-xp').textContent = data.xp.toLocaleString();
                document.getElementById('stat-streak').textContent = data.streak + " DAYS";
            }
        })
        .catch(error => console.error('Error loading stats:', error));
}

function loadDailyChallenge() {
    fetch('/api/dashboard/challenge')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('daily-challenge-container');
            if (data) {
                // Parse JSON content if it's a string, or use as object
                let content = data.Contenido;
                if (typeof content === 'string') {
                    try {
                        content = JSON.parse(content);
                    } catch (e) {
                        content = { description: content };
                    }
                }

                document.getElementById('challenge-title').textContent = data.FocoPrincipal;
                document.getElementById('challenge-desc').textContent = content.description || "Complete the task.";

                // Show button if pending
                if (data.Estado === 'PENDIENTE') {
                    document.getElementById('btn-challenge').style.display = 'block';
                }
            } else {
                container.innerHTML = '<p class="text-center" style="color:#666; padding: 2rem;">No active challenge for today.</p>';
            }
        })
        .catch(error => console.error('Error loading challenge:', error));
}

function loadCourseProgress() {
    fetch('/api/dashboard/progress')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('active-course-container');
            if (data) {
                container.style.display = 'block';
                document.getElementById('course-name').textContent = data.courseName;
                document.getElementById('course-percent-text').textContent = data.percent + "%";
                document.getElementById('course-progress-bar').style.width = data.percent + "%";
            } else {
                container.style.display = 'none'; // Hide if no active course
            }
        })
        .catch(error => console.error('Error loading progress:', error));
}
