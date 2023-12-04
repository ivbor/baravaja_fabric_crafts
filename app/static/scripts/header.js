function changeLanguage(option) {
  console.log('Language changed on ' + option);
}
function handleSelectionChange() {
  var selectedOption = document.getElementById('options').value;
  console.log('Selection changed to ' + selectedOption); 
}
function logout() {
        
  fetch('/logout', {
  
    method: 'GET',
    // Include cookies in the request
    credentials: 'same-origin' 
    
  })
  .then(response => response.json()) 
  .then(data => {
            
    // Check if the logout was successful
    if (data.success) {
                
      // Update the 'logged_in' cookie to 'false'
      document.cookie = 'logged_in=false; path=/';

      // Reload the page
      location.reload();
            
    } else {
                
      // Handle the case when the logout was not successful
      console.error('Logout failed:', data.error);
            
    }
  })
  .catch(error => {
            
    // Handle network errors or other issues
    console.error('Error during logout:', error);
        
  });
}
