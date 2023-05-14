$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

    // });

    // 背景色変更 
    // ----------------------------
    //　処理済み
    $('input[name*=Process]').each(function (i, item) {
        if ($(item).val() == 'Create') {
            $(this).closest('tr').css('background-color', '#A4C6FF');
        }
        if ($(item).val() == 'Delete') {
            $(this).closest('tr').css('background-color', 'gray');
        }
        if ($(item).val() == 'Edit') {
            $(this).closest('tr').css('background-color', '#f0e68c');
        }
    });

    // 既存
    $('input[name*=ExistFlg]').each(function (i, item) {
        console.log(item);
        if ($(item).val() == 'True' || $(item).val() == 1) {
            // $(item).parent().parent().css('color', '#ff0000')
            $(item).closest('tr').css('font-weight', 'bold');
        }
    });

    // 既読
    $('input[name*=ReadFlg]').each(function (i, item) {
        if ($(item).val() == 'True' || $(item).val() == 1) {
            $(this).closest('tr').css('background-color', '#FFFFBB');
        }
    });

    // 削除対象
    $('input[name*=DeleteFlg]').each(function (i, item) {
        if ($(item).val() == 'True' || $(item).val() == 1) {
            $(this).closest('tr').css('background-color', 'gray');
        }
    });

    // 作成対象
    $('input[name*=CreateFlg]').each(function (i, item) {
        if ($(item).val() == 'True' || $(item).val() == 1) {
            $(this).closest('tr').css('background-color', '#A4C6FF');
        }
    });
});


// csrf_tokenの取得に使う
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// 更新中の表示
function spiners(element){
    console.log(element)
    $(element).append('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>')
    return true
}