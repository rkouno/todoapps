$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});
document.querySelectorAll('.toast').forEach(toastNode => {
    const toast = new bootstrap.Toast(toastNode, {
        autohide: false
    });
    toast.show()
});