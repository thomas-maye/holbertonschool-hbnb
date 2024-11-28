/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }
});

async function loginUser(email, password) {
    const apiUrl = 'http://127.0.0.1:5000/api/v1/auth/login';
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();

            document.cookie = `token=${data.access_token}; path=/; Secure`;

            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            displayErrorMessage(errorData.message || 'Invalid login credentials.');
        }
    } catch (error) {
        console.error('Failed to connect to the server:', error);
        displayErrorMessage('Failed to connect to the server. Please try again later.');
    }
}

function displayErrorMessage(message) {
    const errorContainer = document.getElementById('error-message');
    if (errorContainer) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    } else {
        alert(message);
    }
}