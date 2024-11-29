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

    checkAuthentication();
});

// Function to log in the user
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
            document.cookie = "token=" + data.access_token + "; path=/";
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

// Function to display an error message
function displayErrorMessage(message) {
    const errorContainer = document.getElementById('error-message');
    if (errorContainer) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    } else {
        alert(message);
    }
}

// Function to get a cookie value by its name
function getCookieValue(cookieName) {
    const name = cookieName + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookiesArray = decodedCookie.split(';');

    for (let i = 0; i < cookiesArray.length; i++) {
        let cookie = cookiesArray[i].trim();
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return null;
}

// Function to check if the user is authenticated
function checkAuthentication() {
    const token = getCookieValue('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none'; // Hide the login link
        fetchPlaces(token); // Get the places
    }
}

// Function to fetch the places from the API
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Function to display the places
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place';
        placeDiv.setAttribute('data-price', place.price);
        placeDiv.innerHTML = `
            <div class="place-card">
                <h2>${place.title}</h2>
                <p><em>${place.description}</em></p>
                <p><strong>Price: </strong>$${place.price}</p>
                <p><strong>Location: </strong>${place.latitude} ;${place.longitude}</p>
                <button class="details-button" onclick="window.location.href='/place.html?id=${place.id}'">View Details</button>
            </div>
        `;

        placesList.appendChild(placeDiv);
    });
}

// Event listener for the price filter
document.getElementById('price-filter').addEventListener('change', function() {
    const selectedPrice = this.value;
    const places = document.querySelectorAll('#places-list .place');

    places.forEach(place => {
        const placePrice = parseInt(place.getAttribute('data-price'), 10);

        if (selectedPrice === 'all' || placePrice <= selectedPrice) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
});

