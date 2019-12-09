function openForm() {
document.getElementById("popupForm").style.display = "block";
}

function closeForm() {
document.getElementById("popupForm").style.display = "none";
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
                console.log(document.getElementById("desc").value)
            },
            success: function(data, text)
            {

            }
        });
    });