let chartsInstantiated = false;
let marksChartDef = null;
let attChartDef = null;

async function initDashboard() {
    try {
        const stats = await fetchAPI('/dashboard/stats');
        
        document.getElementById('stat-students').textContent = stats.total_students;
        document.getElementById('stat-teachers').textContent = stats.total_teachers;
        document.getElementById('stat-courses').textContent = stats.total_courses;
        document.getElementById('stat-attendance').textContent = stats.attendance_percentage + '%';
        
        if (!chartsInstantiated && window.Chart) {
            const ctxAtt = document.getElementById('attendanceChart').getContext('2d');
            attChartDef = new Chart(ctxAtt, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                    datasets: [{
                        label: 'Attendance Rate',
                        data: [85, 90, 88, 92, 87],
                        borderColor: '#4361ee',
                        tension: 0.4,
                        fill: true,
                        backgroundColor: 'rgba(67, 97, 238, 0.1)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            const ctxMarks = document.getElementById('marksChart').getContext('2d');
            marksChartDef = new Chart(ctxMarks, {
                type: 'doughnut',
                data: {
                    labels: ['A (90-100)', 'B (80-89)', 'C (70-79)', 'Fail (<70)'],
                    datasets: [{
                        data: [40, 30, 20, 10],
                        backgroundColor: ['#4cc9f0', '#4361ee', '#f72585', '#ef233c']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
            chartsInstantiated = true;
        }
    } catch(err) {
        showToast("Error loading dashboard data", "error");
    }
}
