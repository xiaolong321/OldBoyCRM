
$(document).ready(
    function () {
        var da = $.cookie('date');
        if (da == undefined){
            $.cookie('date','desc');
            location.reload()
        }
        else {
            $.cookie('date',da)
        }
        $.each($('.a-ico-sort span '),function (i,n){
            var sort_type = $.cookie($(n).attr('sort_by'));
            if (sort_type == 'desc'|| sort_type=='asc'){
                if (sort_type =='desc'){
                    $(this).parent().siblings().find('.fa-caret-up').addClass('hid')
                }
                else{$(this).parent().siblings().find('.fa-caret-down').addClass('hid')}

            }
        })

    });

// 筛选时排序
$.each($('.a-ico-sort span '),function (i,n) {
    $(n).click(function(){
        var sort_type = $.cookie($(n).attr('sort_by'));
        if(sort_type !== 'undefined'){
        if(sort_type == 'desc'){
            $.cookie($(n).attr('sort_by'),'asc');
        }
        else{
            $.cookie($(n).attr('sort_by'),'desc');

        }
    }})
});





// 禁用排序
$.each($('.fa-ban'),function (i,n) {
    $(n).click(function () {
    var sort_type = $(n).parent().parent().siblings().find('span').attr('sort_by');
        $.removeCookie(sort_type)
    });
});























