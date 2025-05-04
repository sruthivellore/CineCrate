document.addEventListener('DOMContentLoaded', function() {
    let currentForm = null;

    document.querySelectorAll('form.confirm-rent').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            currentForm = this;
            let movieName = form.getAttribute('data-movie-name') || 'this movie';
            document.getElementById('confirmModalLabel').innerText = "Confirm Rent";
            document.querySelector('#confirmModal .modal-body').innerText = `Are you sure you want to rent ${movieName}?`;
            var myModal = new bootstrap.Modal(document.getElementById('confirmModal'));
            myModal.show();
        });
    });

    document.querySelectorAll('form.confirm-return').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            currentForm = this;
            let movieName = form.getAttribute('data-movie-name') || 'this movie';
            document.getElementById('confirmModalLabel').innerText = "Confirm Return";
            document.querySelector('#confirmModal .modal-body').innerText = `Are you sure you want to return "${movieName}"?`;
            var myModal = new bootstrap.Modal(document.getElementById('confirmModal'));
            myModal.show();
        });
    });

    document.getElementById('confirmSubmitBtn').addEventListener('click', function() {
        if (currentForm) {
            currentForm.submit();
        }
    });
});
