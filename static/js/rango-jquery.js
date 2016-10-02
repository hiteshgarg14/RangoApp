$(document).ready(function(){
    // JQuery code to be added in here.
    $("#about-btn").click( function(event) {
        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo"
        $("#msg").html(msgstr)
    });
    $("p").hover(function(){
        $(this).css('color','red');
    },
    function(){
        $(this).css('color','blue');
    });
});
