$('#search-submit').click(function() {

        $.ajax({
            url: "http://titanconnect.pythonanywhere.com/search",
            type: "POST",
            data: JSON.stringify({
                query: document.getElementById("search-form").value,
                //selection: document.getElementById("dropdown").value,
            }),
            dataType: "text", // data type we are expecting in our response from the server
            contentType: "application/json;charset=UTF-8", // data type we are sending to the server
            /*
            beforeSend: function(x)
            {
                if (x && x.overrideMimeType)
                {
                    x.overrideMimeType("application/j-son;charset=UTF-8");
                }
            },*/
            success: function(response)
            {
                console.log(response)
                $("html").html(response)
            }
        });
    });
