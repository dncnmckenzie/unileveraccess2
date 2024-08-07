document.addEventListener("DOMContentLoaded", function () {
    var canvas = document.querySelector("canvas");
    var signaturePad = new SignaturePad(canvas);

    document.getElementById("clear").addEventListener("click", function () {
        signaturePad.clear();
    });

    document.querySelector("form").addEventListener("submit", function (e) {
        if (signaturePad.isEmpty()) {
            alert("Please provide a signature first.");
            e.preventDefault();
        } else {
            var signatureInput = document.getElementById("signature");
            signatureInput.value = signaturePad.toDataURL();
        }
    });
});


