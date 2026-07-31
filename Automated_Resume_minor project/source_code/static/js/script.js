document.addEventListener("DOMContentLoaded", function () {

    console.log("Resume Analyzer Loaded Successfully");

});

function validateForm() {

    let file = document.querySelector('input[type="file"]').value;

    if (file === "") {

        alert("Please upload a resume.");

        return false;

    }

    return true;

}