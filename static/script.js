$(document).ready(function(){
    $("#watchAd").click(function(){
        $.post("/watch_ad", {username: "{{ username }}"}, function(data){
            if(data.balance !== undefined){
                $("#balance").text(data.balance);
                alert("+0.5 credits added!");
            } else {
                alert(data.error);
            }
        });
    });

    $("#withdrawBtn").click(function(){
        $("#withdrawForm").toggle();
    });

    $("#confirmWithdraw").click(function(){
        var amount = $("#withdrawAmount").val();
        $.post("/withdraw", {username: "{{ username }}", amount: amount}, function(data){
            if(data.success){
                alert(data.success);
                $("#balance").text(data.balance);
                $("#withdrawForm").hide();
            } else {
                alert(data.error);
            }
        });
    });
});
