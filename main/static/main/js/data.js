// Handle form submission
document.getElementById('createThreadForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const title = document.getElementById('threadTitle').value.trim();
    const content = document.getElementById('threadContent').value.trim();

    if (!title || !content) return;

    // In a real app, this would send data to a server
    // For now, just redirect back to home
    alert('Thread created successfully!');
    window.location.href = 'index.html';
});
