document.addEventListener('DOMContentLoaded', () => {
    // No script needed for initial static files
});

function deletePost(id) {
    fetch(`/delete/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(() => {
        window.location.reload(); // Refresh the page to see the changes
    });
}
