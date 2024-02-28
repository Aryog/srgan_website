// Function to change button text to loading animation
function showLoading() {
    var button = document.getElementById("pic");
    button.value = "Processing...";
    setInterval(function () {
        button.value = button.value.length < 15 ? button.value + '.' : "Processing...";
    }, 300);
}

// Event listener for form submission
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("pic").addEventListener("click", function () {
        showLoading();
    });
});
