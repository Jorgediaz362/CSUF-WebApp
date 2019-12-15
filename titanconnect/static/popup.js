function openForm() {
document.getElementById("popup-Form").style.display = "block";
}

function closeForm() {
document.getElementById("popup-Form").style.display = "none";
console.log("CLOSING FORM!")
}

$('#submit-reply').click(function() {
        $.ajax({
            url: "/post",
            type: "POST",
            data: JSON.stringify({
                description: document.getElementById("desc").value
            }),
            dataType: "text", // data type we are expecting in our response from the server
            contentType: "application/json;charset=UTF-8", // data type we are sending to the server
            beforeSend: function(x)
            {
                console.log("posting"+document.getElementById("desc").value+"here")
            },
            success: function(data, text)
            {

            }
        });
    });