// alerts fades out after 5 secs

$(document).ready(function() {
    setTimeout(function() {
        $('.alert-dismissible').fadeOut('slow');
    }, 5000);
});