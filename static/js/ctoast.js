    document.addEventListener('DOMContentLoaded', function () {
        const rentButtons = document.querySelectorAll('.show-login-toast');
        const alert = document.getElementById('loginAlert');

        rentButtons.forEach(button => {
            button.addEventListener('click', function () {
                if (alert) {
                    alert.classList.remove('d-none');
                    setTimeout(() => {
                        alert.classList.add('d-none');
                    }, 5000);
                }
            });
        });
    });

