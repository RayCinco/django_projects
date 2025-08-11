document.querySelector('form').addEventListener('submit', function(event) {
    var requiredFields = document.querySelectorAll('input[required], textarea[required]');
    var missingFields = false;

    // Loop through each required field and check if it's empty
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            missingFields = true;
            // Show the popup with a message
            alert(field.getAttribute('placeholder') + " is required");
        }
    });

    // If there are any missing fields, prevent form submission
    if (missingFields) {
        event.preventDefault();  // Prevent form submission
    }
});