$('#like-btn').click(function() {
        $.ajax({
            url: "http://titanconnect.pythonanywhere.com/like",
            type: "POST",
            data: JSON.stringify({
                like_id: window.location.pathname

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