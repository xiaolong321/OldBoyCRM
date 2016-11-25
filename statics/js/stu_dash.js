/**
 * Created by an on 2016/11/13.
 */

//upload.html 页面 删除上传文件
$(document).ready(function () {
    // 删除本次上传的文件
    $('button[class$="file"]').click(function () {
       var file_path = location.pathname;
       var file_name = $(this).parent().siblings()[0].innerText;
       var this_par = $(this).parents('tr');
       $.post(
           '/stu/delete_file/',{'file_path':file_path,'file_name':file_name},
           function (data) {
               if(parseFloat(data) > 0 ){
                   $('.heji').text(data);
                   $(this_par).remove();
               }
               else{
                   $(this_par).parents('table').remove();
                   $('.panel-title:contains("已提交文件")').text('尚未上传文件')
               }
           },'json'
       )
    });



});