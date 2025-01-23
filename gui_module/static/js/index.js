
    // Submit form when "Enter" key is pressed in the textarea
document.getElementById('user_input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent adding a new line
        document.getElementById('chat-form').submit(); // Submit the form
    }
});


    // Function to set focus on the textarea
    function setFocus() {
        document.getElementById('user_input').focus();
    }

    // Attach event listener to the form
    document.getElementById('chat-form').addEventListener('submit', function() {
        // Call setFocus when the form is submitted
        setFocus();
    });

    // Set focus on window load to ensure it happens after the page is rendered
    window.onload = function() {
        setFocus();
    };

    // Scroll to the bottom of the response container whenever new messages are added
    function scrollToBottom() {
        var responseContainer = document.getElementById('response-container');
        responseContainer.scrollTop = responseContainer.scrollHeight;
    }

    // Call this function after loading messages
    scrollToBottom();
   

document.getElementById("btn-chat").addEventListener("click", function() {
        // Show the label
        const labelContainer = document.getElementById("label-container");
        labelContainer.style.display = "block";
  
        // Clear the response container and user input
        
        document.getElementById("user_input").value = "";
    
        const historyList = document.getElementById("history-list");
        const lastSummary = historyList.firstElementChild ? historyList.firstElementChild.textContent : "No previous input.";
  
       const responseContainer = document.getElementById("response-container");
       responseContainer.innerHTML = '<div class="query">${lastSummary}</div>';
 });

// Function to adjust textarea height dynamically
// function autoResizeTextarea() {
//     const textarea = document.getElementById('user_input');
//     textarea.style.height = 'auto'; // Reset height to auto to calculate new height
//     textarea.style.height = `${textarea.scrollHeight}px`; // Set height to scrollHeight
// }
// Function to adjust textarea height dynamically
function autoResizeTextarea() {
    const textarea = document.getElementById('user_input');
    textarea.style.height = 'auto'; // Reset height to auto to calculate new height
    textarea.style.height = `${textarea.scrollHeight}px`; // Set height to scrollHeight
}

// Attach event listener to adjust height on input
document.getElementById('user_input').addEventListener('input', autoResizeTextarea);

// Initial call to adjust height if there's pre-filled text
autoResizeTextarea();
