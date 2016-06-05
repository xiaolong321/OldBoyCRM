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
            action_name: 'classlist',
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
        get_modify: function (event) {
            var self = this;
            var data = {};
            data['pk'] = $(event.target).data('pk');
            data['action'] = $(event.target).data('action');
            var Url = self.send_url;
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
                        self.row_detail(resp.results,'修改', 'post_modify')
                    }
                }
            )
        },
        // 应用全部更改
        application: function (event) {
            var self = this;
            var data = {};
            data['pk'] = $(event.target).data('pk');
            data['action'] = $(event.target).data('action');
            if (data['pk']){
                var __title = '刷新 ID:' + data['pk'] + ' 权限信息!!!';
                var __text = '确认刷新 ID:' + data['pk'] + ' 的权限信息?';
            }
            else{
                var __title = '刷新 全部用户 权限信息!!!';
                var __text = '确认刷新 全部用户信息?';
            }
            swal(
                {
                    title: __title,
                    text: __text,
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定!",
                    cancelButtonText: "取消",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                       setTimeout(
                           function(){
                               var Url = self.send_url;
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
                                            swal(
                                               {
                                                   title:"刷新完毕!",
                                                   timer: 2000,
                                                   showConfirmButton: false
                                               }
                                            );
                                            // 循环 消息内容.
                                            var html_id = '#rbox-footer_status';
                                            $(html_id).empty();
                                            $.each(resp.results,function(key,value){
                                                $(html_id).append(
                                                    value
                                                )
                                            })
                                        }
                                    }
                                )
                           },
                           2000
                       );
                    }
                }
            );
        },
        // 获取详情方法
        get_info: function (event) {
            var self = this;
            var data = {};
            data['pk'] = $(event.target).data('pk');
            data['action'] = $(event.target).data('action');
            var Url = self.send_url;
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
                        self.row_detail(resp.results,'详情')
                    }
                }
            )
        },
        // 获取详情方法
        adds: function (event) {
            var self = this;
            var data = {};
            data['pk'] = $(event.target).data('pk');
            data['action'] = $(event.target).data('action');
            var Url = self.send_url;
            self.row_detail(
                [
                    {
                        'type': 'input',
                        'code': 'name',
                        'name': '账户名',
                        'value': '',
                        'class': '',
                        'disabled': "true",
                    },
                    {
                        'type': 'PositiveSmallIntegerField',
                        'code': 'groups',
                        'name': '用户组',
                        'value': [],
                        'choices': [
                            [1, '管理员'],
                            [2, '运维'],
                            [3, '普通用户'],
                        ],
                        'class': 'pici_1_hosts_class',
                    },
                    {
                        'type': 'Screen',
                        'code': 'userpre',
                        'name': '权限',
                        'value': [],
                        'choices': [
                            {
                                'id':'svn',
                                'name':'svn 权限',
                                'choices':[
                                    {'id': '1', 'name':'svn 测试目录'},
                                    {'id': '1', 'name':'svn 后端'},
                                    {'id': '1', 'name':'svn 前端'},
                                    {'id': '1', 'name':'svn h5'},
                                    {'id': '1', 'name':'svn pc'},
                                    {'id': '1', 'name':'svn 222'},
                                ]
                            },
                            {
                                'id':'vpn',
                                'name':'vpn 权限',
                                'choices':[
                                    {'id': '2', 'name':'青云'}
                                ]
                            },
                            {
                                'id':'qt',
                                'name':'其他权限',
                                'choices':[
                                    {'id': '3', 'name':'测试'}
                                ]
                            },
                        ],
                    }

                ]
                ,'添加','post_add')
            // self.send_issus(
            //     Url,
            //     data,
            //     function (resp) {
            //         console.info(resp);
            //         if(resp.ret_code != 0){
            //             swal({
            //                 title: "错误!",
            //                 text: resp.message,
            //                 type: "error",
            //                 timer: 2000,
            //                 showConfirmButton: false
            //             });
            //         }
            //         else{
            //             self.row_detail(resp.results,'详情')
            //         }
            //     }
            // )
        },
        // 利用传入的 数据.进行菜单创建
        row_detail: function (event, title, Submit) {
            var self = this;
            if(arguments.length === 2){
                var Submit = false;
            }
            // 设定 title 标题
            $(".detail_title").text(title);
            // 清除相关的 内容
            $('.detail_body').empty();
            $('.detail_footer').empty();
            // 循环进行创建
            $.each(event,function(key,value){
                if (value.type == 'input'){
                    $('.detail_body').append(
                        self.row_detail_Input(value, Submit)
                    )
                }
                else if (value.type == 'ManyToManyField') {
                    $('.detail_body').append(
                        self.row_detail_MTMField(value, Submit)
                    )
                }
                else if (value.type == 'PositiveSmallIntegerField'){
                    $('.detail_body').append(
                        self.row_detail_PSIField(value, Submit)
                    )
                }
                else if (value.type == 'TextArea'){
                    $('.detail_body').append(
                        self.row_detail_TextArea(value, Submit)
                    )
                }
                else if (value.type == 'DateField'){
                    $('.detail_body').append(
                        self.row_detail_DateField(value, Submit)
                    )
                }
                else if (value.type == 'Screen'){
                    $('.detail_body').append(
                        self.row_detail_Screen(value, Submit)
                    )
                }
                else if (value.type == 'aggregate'){
                    $('.detail_body').append(
                        self.row_detail_AggReGate(value, Submit)
                    )
                }
                else {
                    console.info('没有检测到 相应格式, key:' + key + " value:" + value);
                }
            });
            // 设定 按牛
            $('.detail_footer').append(
                $.CreateSpan(
                    {
                        'id':'row_detail_dt_status',
                        'style':'color: #EC6868;'
                    },
                    {},
                    ''
                )
            );
            $('.detail_footer').append(
                $.CreateButton(
                    {
                        'type':'button',
                        'data-dismiss': 'modal',
                        'class':'btn btn-default',
                        'v-on:click': "CancelModal('#row_detail_dt')",
                    },
                    {},
                    '取 消'
                )
            );
            if (Submit){
                $('.detail_footer').append(
                    $.CreateButton(
                        {
                            'type':'button',
                            'class':'btn btn-default',
                            'v-on:click': "SubmitModal('#row_detail_dt', '#row_detail_dt_status','row_detail_dt', '"+Submit+"');",
                        },
                        {},
                        '提 交'
                    )
                );
            }

            // 模拟用户点击
            $('#row_detail').click();
            // 从新绘制
            MM_reload_mm();
        },
        // row_detail_DateField
        row_detail_DateField: function (value, Submit) {
            var self = this;
            var tds = [];
            if (value.disabled){
                var disabled = value.disabled;
            }
            else{
                var disabled = false;
            }
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            if (Submit){
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateInput(
                            {
                                'type':'text',
                                'id': 'id_' + value.code,
                                'name':value.name,
                                'value':value.value,
                                'class':'padding-tb-5 form-control' + value.class,
                                'disabled': disabled
                            },
                            {}
                        )
                    )
                )
            }
            else{
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateSpan(
                            {
                                'class': 'padding-tb-5 form-control' + value.class,
                            },
                            {},
                            value.value
                        )
                    )
                )
            }
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // 创建 input 的方法
        row_detail_Input: function (value, Submit) {
            var self = this;
            var tds = [];
            if (value.disabled){
                var disabled = value.disabled;
            }
            else{
                var disabled = false;
            }
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            if (Submit){
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateInput(
                            {
                                'type':'text',
                                'id': 'id_' + value.code,
                                'name':value.name,
                                'value':value.value,
                                'class':'padding-tb-5 form-control' + value.class,
                                'disabled': disabled
                            },
                            {}
                        )
                    )
                )
            }
            else{
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateSpan(
                            {
                                'class': 'padding-tb-5 form-control' + value.class,
                            },
                            {},
                            value.value
                        )
                    )
                )
            }
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // 创建 PositiveSmallIntegerField 方法
        row_detail_PSIField: function (value, Submit) {
            var self = this;
            var tds = [];
            if (value.disabled){
                var disabled = value.disabled;
            }
            else{
                var disabled = false;
            }
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            if (Submit){
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateSelect(
                            {
                                'is-condition':'true',
                                'class':'form-control select-icon no-radius'  + value.class ,
                                'id': 'id_' + value.code,
                                'name':value.name
                            },
                            {},
                            value.choices,
                            value.value,
                            0 ,
                            1
                        )
                    )
                )
            }
            else{
                var value_value = []
                $.each(value.value,function(KEY,VALUE){
                    value_value.push(
                        $.CreateSpan(
                            {},
                            {},
                            VALUE + ','
                        )
                    )
                })
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9',
                            // 'data-value': JSON.stringify(value.value),
                            // 'v-on:MouseMove': "row_Dialog_deploy",
                            // 'v-on:MouseOut': "row_Dialog",
                        },
                        {},
                        value_value
                    )
                )
            }
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // 创建 PositiveSmallIntegerField 方法
        row_detail_MTMField: function (value, Submit) {
            var self = this;
            var tds = [];
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            if (Submit){
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateSelect(
                            {
                                'multiple': "multiple",
                                'is-condition':'true',
                                'class':'form-control select-icon no-radius'  + value.class ,
                                'id': 'id_' + value.code,
                                'name':value.name
                            },
                            {},
                            value.choices,
                            value.value,
                            0 ,
                            1
                        )
                    )
                )
            }
            else{
                var value_value = []
                $.each(value.value,function(KEY,VALUE){
                    value_value.push(
                        $.CreateSpan(
                            {},
                            {},
                            VALUE + ','
                        )
                    )
                })
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9',
                            // 'data-value': JSON.stringify(value.value),
                            // 'v-on:MouseMove': "row_Dialog_deploy",
                            // 'v-on:MouseOut': "row_Dialog",
                        },
                        {},
                        value_value
                    )
                )
            }
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // 创建 PositiveSmallIntegerField 方法
        row_detail_TextArea: function (value, Submit) {
            var self = this;
            var tds = [];
            if (value.disabled){
                var disabled = value.disabled;
            }
            else{
                var disabled = false;
            }
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            if (Submit){
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        $.CreateTextArea(
                            {
                                'id': 'id_' + value.code,
                                'name':value.name,
                                'class':'padding-tb-5 form-control' + value.class
                            },
                            {},
                            value.value
                        )
                    )
                )
            }
            else{
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9'
                        },
                        {},
                        ''
                    )
                )
            }
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // 创建 Screen 自定义多选器
        row_detail_Screen: function (value, Submit) {
            var self = this;
            var tds = [];
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            if (Submit){
                var screen = [];
                var __dl=[];
                __dl.push(
                    $.CreateDt(
                        {},
                        {},
                        '您已经选择:'
                    )
                );
                $.each(value.value,function(key,Val){
                    var screenItem = [];
                    screenItem.push(
                        $.CreateDt(
                            {},
                            {},
                            Val.name
                        )
                    );
                    $.each(Val.choices,function(key,V){
                        screenItem.push(
                            $.CreateDd(
                                {},
                                {},
                                $.CreateA(
                                    {
                                        onclick:"delSel(this, '"+Val.id+"', '"+ V.id +"')",
                                        id:V.id
                                    },
                                    {},
                                    V.name
                                )
                            )
                        )
                    });
                    __dl.push(
                        $.CreateDl(
                            {
                                'class': 'screenItem ',
                                'id': Val.id
                            },
                            {},
                            screenItem
                        )
                    )
                });
                screen.push(
                    $.CreateDl(
                        {
                            'class': 'checkedBox',
                            'name': value.code
                        },
                        {},
                        __dl
                    )
                );
                var screenList = [];
                $.each(value.choices,function(key,Val){
                    var screenItem = [];
                    screenItem.push(
                        $.CreateDt(
                            {},
                            {},
                            Val.name
                        )
                    );
                    $.each(Val.choices,function(key,V){
                        screenItem.push(
                            $.CreateDd(
                                {},
                                {},
                                $.CreateA(
                                    {
                                        onclick:"addSel(this, '"+Val.id+"', '"+ V.id +"')",
                                        id:V.id
                                    },
                                    {},
                                    V.name
                                )
                            )
                        )
                    });
                    screenList.push(
                        $.CreateDl(
                            {
                                'class': 'screenItem ',
                                'id': Val.id
                            },
                            {},
                            screenItem
                        )
                    )
                });
                screen.push(
                    $.CreateDiv(
                        {
                            'class': 'screenList'
                        },
                        {},
                        screenList
                    )
                );
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'screen',
                        },
                        {},
                        screen
                    )
                )
            }
            else{
                var value_value = []
                $.each(value.value,function(KEY,VALUE){
                    value_value.push(
                        $.CreateSpan(
                            {},
                            {},
                            VALUE + ','
                        )
                    )
                })
                tds.push(
                    $.CreateDiv(
                        {
                            'class': 'col-sm-9',
                            // 'data-value': JSON.stringify(value.value),
                            // 'v-on:MouseMove': "row_Dialog_deploy",
                            // 'v-on:MouseOut': "row_Dialog",
                        },
                        {},
                        value_value
                    )
                )
            }
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // 聚合创建
        row_detail_AggReGate: function (value, Submit) {
            var self = this;
            var tds = [];
            tds.push(
                $.CreateLabel(
                    {
                        'class': 'col-sm-2 control-label',
                        'style': 'font-weight: normal'
                    },
                    {},
                    value.name + ':'
                )
            );
            var tds_value = [];
            $.each(value.value,function(Key,Value){
                if (Value.type == 'input'){
                    tds_value.push(
                        self.row_detail_Input(Value, Submit)
                    )
                }
                else if (value.type == 'ManyToManyField') {
                    $('.detail_body').append(
                        self.row_detail_MTMField(value, Submit)
                    )
                }
                else if (Value.type == 'PositiveSmallIntegerField'){
                    tds_value.push(
                        self.row_detail_PSIField(Value, Submit)
                    )
                }
                else if (Value.type == 'TextArea'){
                    tds_value.push(
                        self.row_detail_TextArea(Value, Submit)
                    )
                }
                else if (Value.type = 'aggregate'){
                    tds_value.push(
                        self.row_detail_AggReGate(Value, Submit)
                    )
                }
                else {
                    console.info('没有检测到 相应格式, key:' + key + " value:" + value);
                }
            });
            tds.push(
                $.CreateDiv(
                    {
                        'class': 'col-sm-9'
                    },
                    {},
                    tds_value
                )
            )
            return $.CreateDiv(
                {
                    'class': 'form-group',
                },
                {},
                tds
            )
        },
        // Dialog 方法相关
        row_Dialog_deploy: function (event) {
            var self = this;
            var value = $(event.path).data('value');
            var content = '';
            // console.info([value[0]]);
            $.each(value,function(k,v){
                content += v + ","
            });
            // 取出当前id 的指定内容
            // console.info([content]);
            tripartiteDialog({
                id: 'row_tooltip',
                // align: 'left',
                content: content
            }).show(event.path[0]);
        },
        row_Dialog: function () {
            var a = tripartiteDialog({
                id: 'row_tooltip',
                // align: 'top',
                content: ''
            });
            a.close().remove()
        },
        // 取消
        CancelModal: function(container){
            $(container).find('input').val('');
            $(container).modal('hide');
        },
        // 提交
        SubmitModal: function (formId,statusId,mode_from, action){
            var self = this;
            var data_dict = {};
            var formId_url = formId.split('#')[1].split('_')[1];
            data_dict['mode_from'] = mode_from;
            $(formId).find('input[type="text"]').each(function(){
                var name = $(this).attr('id');
                var val =  $(this).val();
                data_dict[name] = val
            });
            $(formId).find('Select').each(function(){
                var name = $(this).attr('id');
                var val =  $(this).val();
                data_dict[name] = JSON.stringify(val);
            });
            $(formId).find('dl[class="checkedBox"]').each(function () {
                var name = $(this).attr('name');
                var val = [];
                $(this).find('dd').each(function () {
                    val.push(
                        $(this).attr('id')
                    )
                });
                data_dict[name] = JSON.stringify(val);
            })
            // data_dict['pk'] = $(formId).find(id=id_pk_input).html();

            var delUrl = self.send_url;
            data_dict['action'] = action;
            data_dict['action_name'] = this.action_name;

            console.info(data_dict);
            $.AdminLTE.ajaxPost_return(
                     delUrl,
                     data_dict,
                     function (resp) {
                         console.info(resp);
                         callback = resp;
                         if(callback.ret_code != 0){
                             swal({
                                 title: callback.message,
                                 type: "error"
                             }, function (retp) {
                                console.info(callback.message);
                                 // window.location.reload();
                                 //整体执行成功后.重新载入刷新当前页面
                             });
                         }
                         else{
                             swal({
                                 title: callback.message,
                                 type: "success"
                             }, function () {
                                console.info(callback.message);
                                 self.CancelModal(formId);
                                 //整体执行成功后.重新载入刷新当前页面
                             });
                         }
                     }
            );
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
