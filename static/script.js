$(document).ready(function() {

    // Collect credits
    $("#watchAdBtn").click(function() {
        if(!USERNAME) return alert("User not found");
        $.ajax({
            type: "POST",
            url: "/watch_ad",
            contentType: "application/json",
            data: JSON.stringify({username: USERNAME}),
            success: function(data) {
                if(data.balance !== undefined){
                    $("#balance").text(data.balance);
                    alert("+0.5 credits added!");
                } else {
                    alert(data.error);
                }
            },
            error: function() {
                alert("Error updating credits.");
            }
        });
    });

    // Toggle withdraw form
    $("#withdrawBtn").click(function(){
        $("#withdrawForm").toggle();
    });

    // Submit withdraw request
    $("#confirmWithdraw").click(function(){
        const amount = $("#withdrawAmount").val();
        if(!USERNAME) return alert("User not found");
        $.ajax({
            type: "POST",
            url: "/withdraw",
            contentType: "application/json",
            data: JSON.stringify({username: USERNAME, amount: amount}),
            success: function(data){
                if(data.success){
                    alert(data.success);
                    $("#balance").text(data.balance);
                    $("#withdrawForm").hide();
                } else {
                    alert(data.error);
                }
            },
            error: function() {
                alert("Error submitting withdraw request.");
            }
        });
    });
});
