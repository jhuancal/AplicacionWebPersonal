function startExam() {
    const overlay = document.getElementById('exam-start-overlay');
    const container = document.getElementById('exam-form-container');

    if (overlay && container) {
        overlay.style.display = 'none';
        container.style.display = 'block';
    }
}

function selectOption(radio) {
    // Reset siblings
    const container = radio.closest('.options-grid');
    const allBoxes = container.querySelectorAll('.option-box');

    allBoxes.forEach(box => {
        box.style.borderColor = '#444';
        box.style.color = '#aaa';
        box.style.background = '#222';
    });

    // Highlight selected
    const selectedBox = radio.nextElementSibling;
    if (selectedBox) {
        selectedBox.style.borderColor = 'var(--term-gold)';
        selectedBox.style.color = '#fff';
        selectedBox.style.background = '#333';
    }
}

function submitExam() {
    //if (!confirm("Are you sure you want to submit? This action cannot be undone.")) return;

    const form = document.getElementById('course-exam-form');
    if (!form) {
        alert("Error: Exam form not found.");
        return;
    }

    const formData = new FormData(form);
    const data = {};
    data.courseId = formData.get('courseId');
    data.answers = {};

    let hasAnswers = false;
    // Collect answers
    for (let [key, value] of formData.entries()) {
        if (key.startsWith('q')) {
            const qId = key.substring(1);
            data.answers[qId] = value;
            hasAnswers = true;
        }
    }

    if (!hasAnswers) {
        alert("Please answer at least one question before submitting.");
        return;
    }

    const btn = document.querySelector('.btn-submit-exam');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> CALCULATING_RESULTS...';
    }

    fetch('/api/course/exam/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(res => {
            if (res.passed) {
                alert("EXAM PASSED! Score: " + res.score + "%.\n\n+500 XP Awarded.\nCourse Completed!");
                window.location.reload();
            } else {
                alert("EXAM FAILED. Score: " + res.score + "%.\nRequired: " + res.required + "%.\n\nPlease study and try again.");
                window.location.reload();
            }
        })
        .catch(err => {
            console.error(err);
            alert("Internal System Error");
            if (btn) {
                btn.disabled = false;
                btn.textContent = "[ SUBMIT_ANSWERS ]";
            }
        });
}
