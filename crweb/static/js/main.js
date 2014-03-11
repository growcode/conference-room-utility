require([], function () {
    /* Auto refresh the page every 5 minutes */
    var timeout = 5 * 60 * 1000;

    setTimeout(function () {
        window.location.reload(false); 
    }, timeout);

    /* Reload data from the server and refresh the page. */
    $('.force_refresh').on('click', function () {
        $.ajax({
            url: window.location.href + '/reload/1',
            success: function() {
                window.location.reload(false);
            }
        });
        return false;
    });

    /* Go to homepage when the logo is clicked */
    $('.logo').on('click', function () {
        window.location.href = '/';
    });
});
