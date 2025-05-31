let testQuestions = [];
let testAnswers = [];

// Tab switching
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Profile form submission
document.getElementById('profileForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const interests = Array.from(document.querySelectorAll('.checkbox-group input:checked'))
                          .map(cb => cb.value);
    
    const profileData = {
        name: document.getElementById('name').value,
        education: document.getElementById('education').value,
        experience: document.getElementById('experience').value,
        interests: interests,
        skills: document.getElementById('skills').value
    };
    
    try {
        const response = await fetch('/api/save-profile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(profileData)
        });
        
        const result = await response.json();
        if (result.success) {
            showAlert('Profil berhasil disimpan!');
            loadPersonalityTest();
        }
    } catch (error) {
        showAlert('Error: ' + error.message);
    }
});

// Load personality test
async function loadPersonalityTest() {
    try {
        const response = await fetch('/api/personality-test');
        testQuestions = await response.json();
        
        const container = document.getElementById('testContainer');
        container.innerHTML = '';
        
        testQuestions.forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question-container';
            questionDiv.innerHTML = `
                <div class="question-title">${index + 1}. ${q.question}</div>
                <div class="radio-group">
                    ${q.options.map((option, optIndex) => `
                        <label>
                            <input type="radio" name="q${index}" value="${optIndex}" onchange="updateTestProgress()">
                            ${option.text}
                        </label>
                    `).join('')}
                </div>
            `;
            container.appendChild(questionDiv);
        });
    } catch (error) {
        console.error('Error loading test:', error);
    }
}

// Update test progress
function updateTestProgress() {
    const answered = document.querySelectorAll('input[type="radio"]:checked').length;
    document.getElementById('submitTest').disabled = answered < testQuestions.length;
}

// Submit test
async function submitTest() {
    testAnswers = [];
    
    testQuestions.forEach((q, index) => {
        const selected = document.querySelector(`input[name="q${index}"]:checked`);
        if (selected) {
            testAnswers.push(parseInt(selected.value));
        }
    });
    
    try {
        const response = await fetch('/api/submit-test', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({answers: testAnswers})
        });
        
        const result = await response.json();
        if (result.success) {
            showAlert('Tes berhasil diselesaikan!');
            loadRecommendations();
        }
    } catch (error) {
        showAlert('Error: ' + error.message);
    }
}


