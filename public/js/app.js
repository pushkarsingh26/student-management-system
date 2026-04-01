document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('sms_token');
    const userStr = localStorage.getItem('sms_user');
    
    if (!token || !userStr) {
        document.getElementById('login-screen').classList.add('view-active');
        document.getElementById('app-screen').classList.remove('view-active');
        return;
    }
    
    const user = JSON.parse(userStr);
    document.getElementById('login-screen').classList.remove('view-active');
    document.getElementById('app-screen').classList.add('view-active');
    
    document.getElementById('header-user-name').textContent = user.name;
    document.getElementById('header-user-role').textContent = user.role;
    
    const themeBtn = document.getElementById('theme-toggle');
    themeBtn.addEventListener('click', () => {
        const root = document.documentElement;
        if(root.getAttribute('data-theme') === 'dark') {
            root.removeAttribute('data-theme');
            themeBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        } else {
            root.setAttribute('data-theme', 'dark');
            themeBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
    });

    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            navItems.forEach(n => n.classList.remove('active'));
            e.currentTarget.classList.add('active');
            
            const view = e.currentTarget.getAttribute('data-view');
            loadView(view);
        });
    });

    loadView('dashboard');
});

function loadView(viewName) {
    const container = document.getElementById('view-container');
    const template = document.getElementById(`tpl-${viewName}`);
    if (template) {
        container.innerHTML = template.innerHTML;
        if (viewName === 'dashboard' && typeof initDashboard === 'function') initDashboard();
        if (viewName === 'students' && typeof initStudents === 'function') initStudents();
    } else {
        container.innerHTML = '<h2>View not available</h2>';
    }
}

async function exportStudents() {
    try {
        const blob = await fetchAPI('/export/students/csv');
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'students.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        showToast("Error exporting data", "error");
    }
}

async function getInsights() {
    const studentId = document.getElementById('insight-student-id').value;
    if(!studentId) return;
    try {
        const data = await fetchAPI(`/ai/insights/${studentId}`);
        document.getElementById('insight-result').style.display = 'block';
        document.getElementById('ins-prediction').textContent = data.prediction;
        document.getElementById('ins-att').textContent = data.attendance_rate;
        document.getElementById('ins-score').textContent = data.average_score;
        document.getElementById('ins-advice').textContent = data.advice;
        
        let riskClass = 'badge-success';
        if(data.risk_level === 'Medium') riskClass = 'badge-warning';
        if(data.risk_level === 'High') riskClass = 'badge-danger';
        
        const rEl = document.getElementById('ins-risk');
        rEl.textContent = data.risk_level + " Risk";
        rEl.className = `badge ${riskClass}`;
        
    } catch(err) {
        showToast("Failed to fetch AI insights", "error");
    }
}
