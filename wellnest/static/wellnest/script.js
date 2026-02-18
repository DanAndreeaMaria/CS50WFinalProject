// Notification button on the navbar
const bell = document.getElementById("reminderBell");         // 'Notification' in nav
const badge = document.getElementById("reminderBadge");       // '1'
const notification = document.getElementById("notification"); // Message

if (bell) {
    // When the bell is clicked, run the function
    bell.addEventListener("click", function(event) {
        // Prevent going to '#' and runs the custom code
        event.preventDefault();
        // Adds a class called 'show' to the notification element - .notification.show
        notification.classList.add("show");

        // Hides the badge '1' from notifications
        if (badge) {
            badge.style.display = "none";
        }

        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove("show");
        }, 3000);
    });
}



// Saving the form in local storage 
const saveButton = document.getElementById("saveButton");
const entryForm = document.getElementById("entryForm");

if (saveButton && entryForm) {
    saveButton.addEventListener("click", function() {

        // Save flag in browser
        localStorage.setItem("entrySaved", "true");

        // Submit form as usual
        entryForm.onsubmit();
    });
}

// Setting up the message of 'Entry saved'
const flash = document.getElementById("flashMessage");

if (flash && localStorage.getItem("entrySaved") === "true") {

    // Show the message
    flash.style.opacity = 1;

    // Disappear after 3 seconds
    setTimeout(() => {
        flash.style.opacity = 0;
    }, 3000);

    // Remove flag so it doesn't show again
    localStorage.removeItem("entrySaved");
}



// Mood color hints
const cards = document.querySelectorAll(".custom-entry-card");

    // For each element inside 'cards', temporarly call it 'card'
cards.forEach(card => {
    // Get the id from mood inside index
    const moodElement = card.querySelector("#mood-value");

    // If there is no element with 'moodElement' exit function
    if (!moodElement) return;

    // Get the mood and remove whitespaces from beginning & the end
    const mood = moodElement.textContent.trim();

    // Check moods and change colors with proper ones
    if (mood === "Very bad") {
        card.style.borderColor = "#FF4C4C";
    }
    else if (mood === "Bad") {
        card.style.borderColor = "#FF8A65";
    }
    else if (mood === "Neutral") {
        card.style.borderColor = "#FFC107";
    }
    else if (mood === "Good") {
        card.style.borderColor = "#66a369";
    }
    else if (mood === "Very good") {
        card.style.borderColor = "#2ee634";
    }
});
