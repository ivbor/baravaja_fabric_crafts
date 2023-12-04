document.addEventListener('DOMContentLoaded', function () {
    
  // Listen for form submission
  document.getElementById('register-form')
    .addEventListener('submit', function (event) {

      event.preventDefault();

      // Get form data
      var formData = new FormData(this);

      // Make a Fetch request
      fetch('/register', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // Check the response for success
        if (data.success === false) {
          if (data.reason === 'unmatched') {
            if (document.getElementById('wrong-email-message')
              .style.display === 'block') {
          document.getElementById('wrong-email-message')
            .style.display = 'none'; }
          document.getElementById('wrong-password-message')
            .style.display = 'block'; }
          if (data.reason === 'email-exists') {
            if (document.getElementById('wrong-password-message')
              .style.display === 'block') {
          document.getElementById('wrong-password-message')
            .style.display = 'none'; }
          document.getElementById('wrong-email-message')
            .style.display = 'block'; }
        } else {
          window.location.href = '/login';
        }
      })
      .catch(error => {
        // Handle errors if any
        console.error('Error occurred during Fetch request', error);
      });
    });
  });
