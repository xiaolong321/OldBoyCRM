// 列表方法
var CommonListPageVue = Vue.extend({
    el: function(){
        return '#mydataPageVue';
    },
    data: function(){
        return {
            userName: $("#adminlte_page_user_name").val(),
            appName: $("#adminlte_page_app_name").val(),
            modelName: $("#adminlte_page_model_name").val(),
            action_name: 'crm_customer',
            send_url: '/crm/api/issus/', // api 调用的地址
            // 全局刷新接口
            MyReload:false,
            // 解析分页所需全局变量
            // items 总数
            Page_TotalCount:0,
            // 分页数量
            Page_PageSize:20,
            // 当前页面
            Page_PageNumber:1,
            // 页面总数
            Page_TotalPage:1,
            //
            Page_Columns:[],
            // 数据
            Page_Items:[]
        }
    },
    methods: {
        // Dialog 方法相关
        Dialog_restart_pt_deploy: function (event) {
            var self = this;
            var pk = $(event.path).data('pk');
            var field = $(event.path).data('field');
            var content = [];
            // console.info([pk, field]);
            $.each(self.Page_Items,function(key,value){
                if(value.id == pk){
                    // console.info([value.id, pk]);
                    // console.info([value]);
                    if(field == 'groups'){
                        // console.info([value]);
                        content = JSON.stringify(value.groups)
                    }
                    if(field == 'userpre'){
                        // console.info([value]);
                        content = JSON.stringify(value.userpre)
                    }

                }

            });
            // 取出当前id 的指定内容
            // console.info([content]);
            tripartiteDialog({
                id: 'tooltip',
                // align: 'left',
                content: content
            }).show(event.path[0]);
        },
        re_Dialog: function () {
            var a = tripartiteDialog({
                id: 'tooltip',
                // align: 'top',
                content: ''
            });
            a.close().remove()
        },
        // 小工具
        toggleAllBox: function (event) {
            // 快速切换 方法
            $("input[name='checkboxRow']").prop(
                'checked',
                $(event.target).prop('checked')
            );
        },
        // 页面方法
        page: function (event) {
            // 下一页方法
            this.Page_PageNumber = $(event.target).attr('page');
            var static_type = $(event.target).data('type');
            this.loadData(
                // 序列化
                {},
                static_type
            );
        },
        // 二级搜索
        search_ListFilter: function (event) {
            // 查询接口.查询相关的数据
            this.Page_PageNumber = 1;
            var static_type = $(event.target).data('type');
            this.loadData(
                // 序列化
                {},
                static_type
            );
        },
        // 搜索
        search: function (event) {
            // 查询接口.查询相关的数据
            if ($(event.target).data('page')){
                this.Page_PageNumber = $(event.target).data('page');
            }
            var static_type = $(event.target).data('type');
            this.loadData(
                // 序列化
                {},
                static_type
            );
        },
        // 清空查询接口
        resetSearch: function (event) {
            var attr_name = $(event.target).data('name');
            $("#tableSearch_" + attr_name).val('');
            this.search(event);
        },
        // 初始化筛选器
        SlKeySearch: function (data, static_type) {
            var self = this;
            // 初始化 返回列表
            var SlKey = {};
            $('#SlKeySearch').find('input').each(function(){
                var name = $(this).attr('name');
                var val =  $(this).val();
                if(val){
                    SlKey[name] = val;
                    data['PageNumber'] = self.Page_PageNumber;
                }
            });
            if (JSON.stringify(SlKey) != '{}') {
                data['SlKeySearch'] = JSON.stringify(SlKey);
            }
            return data
        },
        //
        SlKeyListFilter: function (data, static_type) {
            var self = this;
            // 初始化 返回列表
            var SlKey = {};
            $('#SlKeyListFilter').find('Select').each(function(){
                var name = $(this).attr('name');
                var val =  $(this).val();
                if(val){
                    SlKey[name] = val;
                    data['PageNumber'] = self.Page_PageNumber;
                }
            });
            if (JSON.stringify(SlKey) != '{}') {
                data['SlKeyListFilter'] = JSON.stringify(SlKey);
            }
            return data
        },
        // 发送接口
        send_issus: function (Url,data,callback,static_type,  sl_key){
            var self = this;
            if(!arguments[5]) sl_key = true;
            data['action_name'] = self.action_name;
            if (sl_key){
                data = self.SlKeyListFilter(data, static_type);
                data = self.SlKeySearch(data, static_type);
            }
            console.info(data);
            $.AdminLTE.ajaxPost_return(
                 Url,
                 data,
                 callback
            );
        },
        // 错误模块
        error_mode: function(Callback, notreload){
            swal({
                title: "失败!"+Callback.message,
                type: "error"
            }, function (retp) {
                console.info(Callback.message);
                // if(notreload!=true){window.location.reload();}
                //整体执行成功后.重新载入刷新当前页面
            });
        },
        // 重载接口
        loadData: function (data, static_type) {
            //
            var self = this;
            // 默认  刷新接口
            data['action'] = 'get_search';
            data['PageSize'] = self.Page_PageSize;
            data['PageNumber'] = self.Page_PageNumber;

            var Url = self.send_url;
            if(arguments.length === 3){
                Url = arguments[2];
            }
            self.send_issus(
                Url,
                data,
                function (resp) {
                    console.info(resp);
                    if(resp.ret_code != 0){
                        swal({
                            title: "错误!",
                            text: resp.message,
                            type: "error",
                            timer: 2000,
                            showConfirmButton: false
                        });
                    }
                    else{
                        self.Page_Items = resp.results;
                        // 每页条数
                        self.Page_PageSize = resp.PageSize;
                        // 当前页面数
                        self.Page_PageNumber = resp.PageNumber;
                        // 总数
                        self.Page_TotalCount = resp.ret_count;
                        // 页面总数
                        self.Page_TotalPage = parseInt(self.Page_TotalCount / self.Page_PageSize) + 1;
                    }
                },
                static_type
            );
        },
        // 自定义内容
        // 修改方法
        get_info: function (event) {
            var self = this;
            var pk = $(event.target).data('pk');
            window.location.href = '/crm/' + 'pages/' + self.action_name + '/?pk=' + pk + '';
        },
        // 跳转到详情页面
        get_adds:function (event) {
            var self = this;
            var pk = $(event.target).data('pk');
            window.location.href = '/crm/' + 'pages/' + self.action_name + '/?add=ok';
        }
    }
});


var mydataPageVue = new CommonListPageVue({
    ready: function () {
    }
});

function MM_reload_mm(formId,statusId){
    var mydataPageVue = new CommonListPageVue({
        ready: function () {
        }
    });
}
