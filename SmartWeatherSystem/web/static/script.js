let currentUser = null;

// Form submission handlers
function handleLoginSubmit(event) {
    event.preventDefault();
    login();
}

function handleRegisterSubmit(event) {
    event.preventDefault();
    register();
}

async function register() {
    try {
        console.log('Register function called');
        const username = document.getElementById('regUser').value;
        const password = document.getElementById('regPass').value;
        const hostCity = document.getElementById('regCity').value;

        console.log('Sending registration data:', { username, password, host_city: hostCity });

        if (!username || !password || !hostCity) {
            alert('Please fill in all fields');
            return;
        }

        console.log('Attempting to fetch /api/register...');
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, host_city: hostCity })
        });

        console.log('Fetch completed. Status:', res.status, 'OK:', res.ok);
        const data = await res.json();
        console.log('Response data:', data);

        if (res.ok) {
            console.log('Registration successful');
            alert("Registered! Please login.");
            // Clear form fields
            document.getElementById('regUser').value = '';
            document.getElementById('regPass').value = '';
            document.getElementById('regCity').value = '';
        } else {
            console.log('Registration failed:', data.error);
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Register error:', error);
        alert('Error: ' + error.message);
    }
}

async function login() {
    try {
        console.log('Login function called');
        const username = document.getElementById('loginUser').value;
        const password = document.getElementById('loginPass').value;

        console.log('Sending login data:', { username, password });

        if (!username || !password) {
            alert('Please enter username and password');
            return;
        }

        console.log('Attempting to fetch /api/login...');
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        console.log('Fetch completed. Status:', res.status, 'OK:', res.ok);
        const data = await res.json();
        console.log('Response data:', data);

        if (res.ok) {
            console.log('Login successful. User ID:', data.user_id);
            console.log('Redirecting to weather page...');
            // Redirect to weather page with user data
            const redirectUrl = `/weather?user_id=${data.user_id}&username=${encodeURIComponent(data.username)}&host_city=${encodeURIComponent(data.host_city)}`;
            console.log('Redirect URL:', redirectUrl);
            setTimeout(() => {
                window.location.href = redirectUrl;
            }, 100);
        } else {
            console.log('Login failed:', data.error);
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Error: ' + error.message);
    }
}

function logout() {
    currentUser = null;
    window.location.href = '/';
}

function handleSearchSubmit(event) {
    event.preventDefault();
    fetchWeather();
}

async function fetchWeather() {
    const city = document.getElementById('cityInput').value;
    if (!city) return;

    try {
        const res = await fetch(`/api/weather?city=${city}&user_id=${currentUser.user_id}`);
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // 1. Render Current
        const main = data.current.main;
        const weather = data.current.weather[0];
        const wind = data.current.wind || {};
        const sys = data.current.sys || {};
        document.getElementById('currentData').innerHTML = `
            <div class="temp-display">${Math.round(main.temp)}°C</div>
            <div><strong>Condition:</strong> ${weather.description.charAt(0).toUpperCase() + weather.description.slice(1)}</div>
            <div><strong>Weather Type:</strong> ${weather.main}</div>
            <div><strong>Humidity:</strong> ${main.humidity}%</div>
            <div><strong>Wind Speed:</strong> ${wind.speed || 'N/A'} m/s</div>
            <div><strong>Country:</strong> ${sys.country || 'N/A'}</div>
        `;

        // 2. Render Alert
        const alertBanner = document.getElementById('alertBanner');
        if (data.system_alert) {
            alertBanner.innerText = data.system_alert;
            alertBanner.classList.remove('hidden');
        } else {
            alertBanner.classList.add('hidden');
        }

        // 3. Render Forecast
        const forecastDiv = document.getElementById('forecastData');
        forecastDiv.innerHTML = '';
        if (data.forecast && data.forecast.list) {
            // API already returns daily data (8 days), so show all of them
            data.forecast.list.forEach(day => {
                const date = new Date(day.dt * 1000).toLocaleDateString();
                forecastDiv.innerHTML += `
                    <div class="forecast-item">
                        <span>${date}</span>
                        <span>${Math.round(day.main.temp)}°C</span>
                        <span>${day.weather[0].main}</span>
                    </div>
                `;
            });
        }

        // 4. Refresh History
        fetchHistory();

    } catch (e) {
        console.error(e);
        alert('Error fetching weather: ' + e.message);
    }
}

let allHistoryLogs = []; // Store all history for filtering

async function fetchHistory() {
    try {
        const res = await fetch(`/api/history/${currentUser.user_id}`);
        allHistoryLogs = await res.json();
        renderHistory(allHistoryLogs);
    } catch (e) {
        console.error('Error fetching history:', e);
    }
}

function renderHistory(logs) {
    const historyDiv = document.getElementById('historyData');
    if (logs.length === 0) {
        historyDiv.innerHTML = '<p>No history found</p>';
        return;
    }
    historyDiv.innerHTML = logs.map(log => `
        <div class="history-item">
            <span><strong>Date:</strong> ${log.date}</span>
            <span><strong>City:</strong> ${log.city}</span>
            <span><strong>Temp:</strong> ${log.temp}°C</span>
        </div>
    `).join('');
}

function applyHistoryFilter() {
    const cityFilter = document.getElementById('filterCity').value.toLowerCase();
    const dateFilter = document.getElementById('filterDate').value;

    let filtered = allHistoryLogs;

    if (cityFilter) {
        filtered = filtered.filter(log => log.city.toLowerCase().includes(cityFilter));
    }

    if (dateFilter) {
        filtered = filtered.filter(log => log.date.startsWith(dateFilter));
    }

    renderHistory(filtered);
}

function clearHistoryFilter() {
    document.getElementById('filterCity').value = '';
    document.getElementById('filterDate').value = '';
    renderHistory(allHistoryLogs);
}

// Initialize weather page on load
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    console.log('Current URL:', window.location.href);

    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    const username = urlParams.get('username');
    const hostCity = urlParams.get('host_city');

    console.log('URL Parameters - userId:', userId, 'username:', username, 'hostCity:', hostCity);

    const displayUserElement = document.getElementById('displayUser');
    console.log('displayUser element exists:', !!displayUserElement);

    // Only initialize if we're on the weather page with user data
    if (userId && username && hostCity && displayUserElement) {
        console.log('Initializing weather page with user data');
        currentUser = { user_id: userId, username: username, host_city: hostCity };
        document.getElementById('displayUser').innerText = currentUser.username;
        document.getElementById('displayHost').innerText = currentUser.host_city;
        document.getElementById('cityInput').value = currentUser.host_city;

        // Setup weather page buttons
        const searchBtn = document.getElementById('searchBtn');
        const logoutBtn = document.getElementById('logoutBtn');

        if (searchBtn) {
            searchBtn.addEventListener('click', fetchWeather);
        }
        if (logoutBtn) {
            logoutBtn.addEventListener('click', logout);
        }

        console.log('Fetching initial weather for city:', currentUser.host_city);
        fetchWeather();
    } else {
        console.log('Not on weather page or missing parameters');
    }
});