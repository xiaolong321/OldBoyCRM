
$(document).ready(
    function () {
        var da = $.cookie('date');
        var cur_url_name=location.pathname.split('/')[2].split('-')[0];
        var page_content_hr = $('#page-content').attr('href_pathname');
        $.each($('.a-ico-sort span '),function (i,n){
            var sort_type = $.cookie($(n).attr('sort_by'));

            if (sort_type == 'desc'|| sort_type=='asc'){
                if (sort_type =='desc'){
                    $(this).parent().siblings().find('.fa-caret-up').addClass('hid');
                }
                else{
                    $(this).parent().siblings().find('.fa-caret-down').addClass('hid');
                }

            }
        })

    });

// 筛选时排序
$.each($('.a-ico-sort span '),function (i,n) {
    $(n).click(function(){

        var sort_type = $.cookie($(n).attr('sort_by'));
        if(sort_type !== 'undefined'){
            if(sort_type == 'desc'){
                 $.each($.cookie(),function (i,n) {
                    if(n=='desc' ||n=='asc'){
                        $.removeCookie(i)
                    }
                     });
                $.cookie($(n).attr('sort_by'),'asc');
            }
            else{
                 $.each($.cookie(),function (i,n) {
            if(n=='desc' ||n=='asc'){
                $.removeCookie(i)
            }
        });
                $.cookie($(n).attr('sort_by'),'desc');

            }
    }})
});



























