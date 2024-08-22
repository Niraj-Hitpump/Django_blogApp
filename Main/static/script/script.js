// script code for the login
function login(event) {
    event.preventDefault();

    var username = document.getElementById("floatingInput").value;
    var password = document.getElementById("floatingPassword").value;
    var csrf = document.getElementById('csrf').value;

    if (username === '' || password === '') {
        alert("Please Enter Both Username and Password.");
        return;
    }

    var data = {
        username: username,
        password: password
    };
    
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body: JSON.stringify(data),
    }).then(result => result.json())
    .then(response => {
        console.log(response);
    }).catch(error => {
        console.error('Error:', error);
    });
}