
$(document).ready(
    function () {
        var da = $.cookie('date');
        var cur_url_name=location.pathname.split('/')[2].split('-')[0];
        var page_content_hr = $('#page-content').attr('href_pathname');

       // 页面为dashboard页面时,不要在cookie中添加date键，否则会扰乱其他页面默认排序
       // 当新页面cookie中没有 date 键时，且配需中有按date默认排序的需求时要自动添加date，实现默认排序
      if (da == undefined && cur_url_name ==page_content_hr ){
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























