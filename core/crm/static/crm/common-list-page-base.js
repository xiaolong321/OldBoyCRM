var CommonListPageVue = Vue.extend({
    el: function(){
        return '#commonDataTableRow';
    },
    data: function(){
        return {
            // 基础设定
            // 当前账户名称
            userName: $("#adminlte_page_user_name").val(),
            // action
            action: $("#adminlte_page_action").val(),
            // action_name
            action_name: $("#adminlte_page_action_name").val(),
            // url 基础
            Url:'/crm',
            // 列表设定
            // items 主循环列表
            items: [
            ],
            // 当前页面
            currentPage: 1,
            // 总页数
            totalPage: 1,
            // 每页数量
            perPage: 10,
            // 总数
            count: 0,
            // 计算当前 是那列
            sortKey: '',
            // 初始化各种列
            sortOrders: {},
            //
            filterKey: '',
            columns:[],
            grifcolumns: [],
            // 其他设定
            searchQuery: ''
        }
    },
    methods: {
        // 小工具
        toggleAllBox: function (event) {
            // 快速切换 方法
            $("input[name='checkboxRow']").prop(
                'checked',
                $(event.target).prop('checked')
            );

            // 反选
            // $("input[name='checkboxRow']").each(function () {
            //     this.checked = !this.checked;
            //  })
            // 全选
            // $("#btnAllChk").click(function () {
            //     $("#chk input:checkbox").attr("checked", "checked");
            // });
            // 全不选
            // $("#btnAllNotChk").click(function () {
            //     $("#chk input:checkbox").removeAttr("checked");
            // });
        },
        sortBy: function (KEY) {
            // var key = $(event.target).data('pk');
            console.info(KEY);
            var self = this;
            self.grifcolumns.forEach(function (key) {
                if (KEY != key ){
                    self.sortOrders[key] = 1
                }
            });
            self.sortKey = KEY;
            self.sortOrders[KEY] = this.sortOrders[KEY] * -1;

            console.info(
                'sortKey:' + self.sortKey +
                ' sortOrders:' + self.sortOrders[KEY]
            );
        },
        // 页面方法
        page: function (event) {
            // 下一页方法
            var num = $(event.target).attr('page');
            this.loadData({'page': num});
        },
        // get 方法解决
        detail: function (event) {
            // 详情方法
            var self = this;
            var pk = $(event.target).data('pk');
            window.location.href = self.Url + '/pages/' + self.action_name + '/?pk=' + pk;
        },
        update: function (event) {
            // 修改方法
            // 修改与详情一样 都是直接 跳转到相应的页面
            var self = this;
            self.detail(event)
        },
        create: function (event, modelName) {
            // 创建方法
            var self = this;
            window.location.href = self.Url + '/pages/' + self.action_name + '/?add=create';
        },
        // post 方法
        remove: function (ids) {
            // 删除方法
            // 删除后 在上方消息框打印相关内容
            var self = this;
            var Url = self.Url + '/api/issue';
            swal({
                title: "确定要删除吗?",
                text: "您确定要删除所选数据吗?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定!",
                cancelButtonText: "取消",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                self.send_issus(
                    Url,
                    {
                        'remove_list': JSON.stringify(ids),
                        'action': 'remove'
                    },
                    function (resp) {
                        console.info(resp);
                        //callback = $.parseJSON(resp);
                        callback = resp;
                        if(!callback.status){
                            swal({
                                title: "删除失败!"+callback.message,
                                type: "error"
                            }, function () {
                                self.loadData({});                                                                          //整体执行成功后.重新载入刷新当前页面
                            });
                        }else{
                            swal({
                                title: "删除成功!",
                                type: "success"
                            }, function () {
                                self.loadData({});                                                                          //整体执行成功后.重新载入刷新当前页面
                            });
                        }
                    }
                );
            });
        },
        removeSelected: function () {
            // 批量删除 选定
            var ids = [],
                box = $("input[name='checkboxRow']:checked");
            $.each(box, function (i, b) {
                ids.push($(b).val());
            });
            if (ids.length === 0) {
                swal({
                    title: "请选择数据!",
                    type: "warning"
                });
                return;
            }
            this.remove(ids);
        },
        removeOne: function (event) {
            // 单独删除
            this.remove([$(event.target).data('pk')]);
        },
        // 搜索
        search: function (event) {
            // 查询接口.查询相关的数据
            this.loadData(
                // 序列化
                {}
            );
        },
        resetSearch: function (event) {
            // 清空查询接口
            $("#tableSearch").val('');
            this.search(event);
        },
        // 初始化筛选器
        sl_key: function (data) {
            // 初始化 返回列表
            var ret = {};
            $('#sl-key').find('Select').each(function(){
                var name = $(this).attr('name');
                var val =  $(this).val();
                ret[name] = val
            });
            data['search_key'] = JSON.stringify(ret);
            data['search'] = JSON.stringify({'qq':$("#tableSearch").val()});
            return data
        },
        // 获取与 刷新数据
        send_issus: function (Url,data,callback, sl_key){
            var self = this;
            if(!arguments[4]) sl_key = true;
            data['action_name'] = self.action_name;
            if (sl_key){
                data = self.sl_key(data);
            }
            console.info(data);
            $.AdminLTE.ajaxPost_return(
                 Url,
                 data,
                 callback
            );
        },
        error_mode: function(Callback, notreload){
            swal({
                title: "失败!"+Callback.message,
                type: "error"
            }, function (retp) {
                console.info(Callback.message);
                if(notreload!=true){window.location.reload();}
                //整体执行成功后.重新载入刷新当前页面
            });
        },
        loadData: function (data) {
            var self = this;
            var Url = self.Url + '/api/issue';
            if(arguments.length === 2){
                Url = arguments[1];
            }
            data['action'] = self.action;
            self.send_issus(
                Url,
                data,
                function (resp) {
                    console.info(resp);
                    self.items = resp.results;
                    self.count = resp.count;
                    self.perPage = resp.per_page;
                    self.totalPage = resp.total_page;
                    self.currentPage = resp.current_page;
                }
            );
        }
    }
});
