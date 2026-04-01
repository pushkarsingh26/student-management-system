document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            const errorP = document.getElementById('login-error');
            
            try {
                const formData = new URLSearchParams();
                formData.append('username', email);
                formData.append('password', password);
                
                const data = await fetchAPI('/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: formData.toString()
                });
                
                localStorage.setItem('sms_token', data.access_token);
                
                const profile = await fetchAPI('/auth/me');
                localStorage.setItem('sms_user', JSON.stringify(profile));
                
                showToast("Login successful!");
                setTimeout(() => window.location.reload(), 500);
            } catch (err) {
                errorP.textContent = err.message;
            }
        });
    }

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('sms_token');
            localStorage.removeItem('sms_user');
            window.location.reload();
        });
    }
});
