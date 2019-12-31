$(document).ready(function () {
    $('#characterLeft').text('140 characters left');
    $('#message').keydown(function () {
        var max = 140;
        var len = $(this).val().length;
        if (len >= max) {
            var str = "You have reached the limit";
            var result = str.fontcolor("red")
            document.getElementById("characterLeft").innerHTML = result;
            $('#characterLeft').text().addClass('red');
            $('#btnSubmit').addClass('disabled');
        }
        else {
            var ch = max - len;
            $('#characterLeft').text(ch + ' characters left');
            $('#btnSubmit').removeClass('disabled');
            $('#characterLeft').removeClass('red');
        }
    });
});

function show_spous_name() {
    if (document.getElementById('married').checked) {
        document.getElementById('marital').style.visibility = 'visible';
    } else {
        document.getElementById('marital').style.visibility = 'hidden';
    }
}

