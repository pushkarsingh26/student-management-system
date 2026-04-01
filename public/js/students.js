let currentPage = 0;
const perPage = 10;
let currentSearch = "";
let searchTimeout = null;

async function initStudents() {
    currentPage = 0;
    document.getElementById('student-search').value = "";
    await fetchStudents();
}

async function fetchStudents() {
    try {
        const data = await fetchAPI(`/students/?skip=${currentPage * perPage}&limit=${perPage}&search=${currentSearch}`);
        
        const tbody = document.getElementById('student-table-body');
        tbody.innerHTML = '';
        
        data.data.forEach(student => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><b>${student.enrollment_no}</b></td>
                <td>
                    <div style="display:flex; align-items:center; gap:10px">
                        <img src="${student.profile_pic || 'https://ui-avatars.com/api/?name='+student.name+'&background=random'}" style="width:30px; height:30px; border-radius:50%; object-fit:cover">
                        ${student.name}
                    </div>
                </td>
                <td>${student.email}</td>
                <td>${student.age}</td>
                <td>
                    <button class="btn btn-icon btn-secondary" onclick="viewStudent(${student.id})"><i class="fa-solid fa-eye"></i></button>
                    <button class="btn btn-icon btn-danger" onclick="deleteStudent(${student.id})"><i class="fa-solid fa-trash"></i></button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        
        const totalPages = Math.ceil(data.total / perPage) || 1;
        document.getElementById('page-info').textContent = `Page ${currentPage + 1} of ${totalPages}`;
        
        document.getElementById('prev-btn').disabled = currentPage === 0;
        document.getElementById('next-btn').disabled = currentPage >= totalPages - 1;
        
    } catch(err) {
        showToast("Error fetching students", "error");
    }
}

function debounceSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        currentSearch = document.getElementById('student-search').value;
        currentPage = 0;
        fetchStudents();
    }, 500);
}

function nextPage() {
    currentPage++;
    fetchStudents();
}

function prevPage() {
    if(currentPage > 0) {
        currentPage--;
        fetchStudents();
    }
}

async function deleteStudent(id) {
    if(!confirm("Are you sure you want to delete this student?")) return;
    try {
        await fetchAPI(`/students/${id}`, { method: 'DELETE' });
        showToast("Student deleted successfully");
        fetchStudents();
    } catch(err) {
        showToast("Error deleting student: " + err.message, "error");
    }
}

function viewStudent(id) {
    showToast("Opening student profile...");
}

function openStudentModal() {
    showToast("Add Student feature to be implemented natively.");
}
