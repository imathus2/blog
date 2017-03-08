$(document).ready(function () {
    
    //Initialize mobile side nav
    $(".button-collapse").sideNav();
    
    // Initialize materialize tooltip
    $('.tooltipped').tooltip({delay: 50});

    // No of comments on posts
    size = $("#commentList li").length;
    // Hide view more button if no comment
    if (size == 0)
    {
        $('#viewMore').hide();
        $('#noComments').show();
    }
    x=2;
    //Shows 2 more comments on view more button click
    $('#commentList li:lt('+x+')').show();
    $('#viewMore').click(function () {
        x= (x+2 <= size) ? x+2 : size;
        $('#commentList li:lt('+x+')').show();
        if (x == size) {
            $('#viewMore').addClass("disable");
        }	
    });
});
