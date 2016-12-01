/**
 * Created by Administrator on 2016/9/26 0026.
 */
// 发布输入框， 字数统计
$.event.special.valuechange = {

    teardown: function (namespaces) {
        $(this).unbind('.valuechange');
    },

    handler: function (e) {
        $.event.special.valuechange.triggerChanged($(this));
    },

    add: function (obj) {
        $(this).on('keyup.valuechange cut.valuechange paste.valuechange input.valuechange', obj.selector, $.event.special.valuechange.handler)
    },

    triggerChanged: function (element) {
        var current = element[0].contentEditable === 'true' ? element.html() : element.val()
            , previous = typeof element.data('previous') === 'undefined' ? element[0].defaultValue : element.data('previous')
        if (current !== previous) {
            element.trigger('valuechange', [element.data('previous')]);
            element.data('previous', current)
        }
    }
};

$(function () {
    $('#saytext').on('valuechange', function (e, previous) {
        var val_length = $(this).val().length;
        var new_length = 140 - val_length;
        if (new_length <= 0) {
            var temp = "已超出<span style='color: red'>" + (-new_length) + "</span>字";
            $('.num').html(temp);
            $('.W_btn_a_disable').css({'background': '#ddd', 'color': 'black'});
            $('#publish-button').attr('onclick', '');
        } else {
            var len = "还可以输入<span>" + new_length + "</span>字";
            $('.num').html(len);
            $('.num span').text(new_length);
            $('.W_btn_a_disable').css({'background': '#ffc09f', 'color': '#fff'});
            $('#publish-button').attr('onclick', 'publish()');
        }
    })
});

//发布动态
function publish() {
    var temp = '<span>'+replace_em($('#saytext').val())+'</span>';
    var enter_text = $(temp).get(0);
    var qq_img = $(enter_text).children('img');
    $(qq_img).each(function () {
        var qq_img_src =  "../../Statics/UIHomePage/Images/" + $(this).attr('src');
        $(this).attr('src', qq_img_src);
        console.log(qq_img_src);
    });
    var img_list = document.getElementById('upload').files;
    var zane = $('#zane').html();
    var element = $(zane).get(0);
    $(element).find('#enter_text').html(enter_text);
    $(img_list).each(function () {
        var img = document.createElement('img');
        var li = document.createElement('li');
        $(img).attr('src', window.URL.createObjectURL(this));
        $(li).addClass('WB_pic li_1 S_bg1 S_line2 bigcursor"');
        $(li).append(img);
        $(element).find('#new_picture').append(li);
    });
    $(element).insertAfter('#home_new_feed_tip');
    $('.layer_pic_list').css('display', 'none');
    $('#preview').text('');
    $('#saytext').val('');
    $('#upload').val('');

}