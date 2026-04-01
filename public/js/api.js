const API_BASE = window.location.origin.includes("127.0.0.1") || window.location.origin.includes("localhost") 
    ? "http://127.0.0.1:8000/api" 
    : "/api";

function showToast(message, type="success") {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fa-solid ${type === 'success' ? 'fa-check-circle' : 'fa-triangle-exclamation'}"></i>
        <span>${message}</span>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function fetchAPI(endpoint, options = {}) {
    const token = localStorage.getItem('sms_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (options.body instanceof FormData) {
        delete headers['Content-Type'];
    }

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });

        if (res.status === 401) {
            localStorage.removeItem('sms_token');
            localStorage.removeItem('sms_user');
            window.location.reload();
            return null;
        }
        
        // Handle Blob for export
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("csv")) {
            return await res.blob();
        }

        const data = await res.json();
        
        if (!res.ok) {
            throw new Error(data.detail || data.message || 'Something went wrong');
        }

        return data;
    } catch (err) {
        throw err;
    }
}
