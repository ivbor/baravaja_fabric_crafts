document.addEventListener('DOMContentLoaded', function () {
    
  // Listen for form submission
  document.getElementById('login-form')
    .addEventListener('submit', function (event) {

      event.preventDefault();

      // Get form data
      var formData = new FormData(this);

      // Make a Fetch request
      fetch('/login', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // Check the response for success
        if (data.success === false) {
          // Display the login-message
          document.getElementById('login-message').style.display = 'block';
        } else {
          document.cookie = 'logged_in=true; path=/';
          window.location.href = '/home';
        }
      })
      .catch(error => {
        // Handle errors if any
        console.error('Error occurred during Fetch request', error);
      });
    });
  });
