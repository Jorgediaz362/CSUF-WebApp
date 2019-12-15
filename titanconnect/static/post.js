$('#createpostbtn').click(function() {
        $.ajax({
            url: "/newpost",
            type: "POST",
            data: JSON.stringify({
                title: document.getElementById("title").value,
                description: document.getElementById("desc").value
            }),
            dataType: "text", // data type we are expecting in our response from the server
            contentType: "application/json;charset=UTF-8", // data type we are sending to the server
            /*beforeSend: function(x)
            {
                if (x && x.overrideMimeType)
                {
                    x.overrideMimeType("application/j-son;charset=UTF-8");
                }
            },*/
            success: function(data, text)
            {

            }
        });
    });