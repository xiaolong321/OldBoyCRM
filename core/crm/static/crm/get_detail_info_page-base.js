var MydataPageVue = Vue.extend({
    el: function(){
        return '#mydataPageVue';
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
                 {
                     'mode': false,
                     'code':'s',
                     'title':'测试',
                     'data':[{'name':'测试', 'type':'input', 'code':'12', 'data':'heihei'}]
                 }
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
            searchQuery: '',
            nid:$("#nid").val()
        }
    },
    methods: {
        get_web_file: function (event) {
            var self = this;
            window.location.href = self.Url + '/pages/' + 'web_file' + '/?pk=' + self.nid;
        },
        get_items_code: function (code) {
            var self = this;
            var item = {};
            $.each(self.items,function(key,value){
                if(code == value.code){
                    item = value
                }
            });
            return item
        },
        hosts_info_modify:  function(event){
            var self = this;
            var data = {};
            var instance_id = $(event.target).data('pk');
            var my_code = $(event.target).data('code');
            var items = self.get_items_code(my_code);
            var html_lod = $(event.path[2]).find('div');
            var my_tbody = $(html_lod[2]).find('tbody');
            data['action'] = 'hosts_info_modify';
            data['action_name'] = self.appName;
            var hosts_info_html_new = [];
            $.each(items.data,function(key,value){
                var tds = [];
                var it_data = '';
                if(value.type == 'PositiveSmallIntegerField'){
                    it_data = $.CreateSelect(
                        {
                            'is-condition':'true',
                            'class':'form-control select-icon no-radius',
                            'id':"id_" + value.code,
                            'name':value.code
                        },
                        {}, 
                        value.get_choices,
                        value.data,
                        0 ,
                        1
                    );
                }else if(value.type == 'ManyToManyField'){
                    it_data = $.CreateSelect(
                        {
                            'multiple': "multiple",
                            'is-condition':'true',
                            'class':'form-control select-icon no-radius',
                            'id':"id_" + value.code,
                            'name':value.code
                        },
                        {},
                        value.get_choices,
                        value.data,
                        0 ,
                        1
                    );
                }else if(value.type == 'ForeignKey'){
                    it_data = $.CreateSelect(
                        {
                            'is-condition':'true',
                            'class':'form-control select-icon no-radius',
                            'id':"id_" + value.code,
                            'name':value.code
                        },
                        {},
                        value.get_choices,
                        value.data,
                        0 ,
                        1
                    );
                }else {
                    it_data = $.CreateInput(
                        {'type':'text','name':value.code,'value':value.data,'class':'padding-tb-5 form-control'},
                        {'width':'100%'})
                }
                tds.push($.CreateTd({},{},value.name+':'));
                if(value.no_input == true){
                    tds.push($.CreateTd({}, {}, value.data));
                }else{
                    tds.push($.CreateTd({}, {}, it_data));
                }
                var tr = $.CreateTr({},{},tds);
                hosts_info_html_new.push(tr);


            });
            my_tbody.find('tr').remove();
            my_tbody.append(hosts_info_html_new);
            $(html_lod[1]).find('button').remove();
            $(html_lod[1]).append('<button ' +
                'class="btn btn-primary"'+
                'data-pk="' + instance_id + '"'+
                'v-on:click="info_modify_cancel"><i class="fa fa-plus"></i>'+
                '取消'+
                '</button>'
            );
            $(html_lod[1]).append('<button ' +
                'class="btn btn-primary"'+
                'data-pk="' + instance_id + '"'+
                'v-on:click="info_modify_save"><i class="fa fa-plus"></i>'+
                '保存'+
                '</button>'
            );

            MM_reload_mm()

            $.each(items.data,function(key,value){
                if(value.type == 'ManyToManyField') {
                    $("#id_" + value.code).select2(
                        {
                            placeholder: "请选择",
                        }
                    );
                }
            });
        },
        info_modify_cancel: function(event){
            window.location.reload();
        },
        info_modify_save: function(event){
            var self = this;
            var instance_id = $(event.target).data('pk');
            var my_code = $(event.target).data('code');
            var items = self.get_items_code(my_code);
            var html_lod = $(event.path[3]).find('div');
            var my_tbody = $(html_lod).find('tbody');

            var data_dict = {};
            var DData_dict = {};
            my_tbody.find('input[type="text"]').each(function(){
                var name = $(this).attr('name');
                var val =  $(this).val();
                DData_dict[name] = val
            });
            my_tbody.find('Select').each(function(){
                var name = $(this).attr('name');
                var val =  $(this).val();
                if (val){
                    DData_dict[name] = val
                }
            });

            data_dict['id'] = $(event.target).data('pk');
            data_dict['data'] = JSON.stringify(DData_dict);
            data_dict['action'] = 'post_' + self.action;
            setTimeout(self.send_issus(
                self.Url + '/api/issus/',
                data_dict,
                function (resp) {
                    console.info(resp);
                    callback = resp;
                    if(callback.ret_code != 0){
                        self.error_mode(resp ,notreload=true)
                    }else{
                        swal({
                            title: '保存成功',
                            type: "success"
                        }, function () {
                            console.info(callback.message);
                            window.location.reload()
                        });
                    }
                }
            ),20000);
        },
        // 获取与 刷新数据
        send_issus: function (Url,data,callback,sl_key){
            var self = this;
            if(!arguments[4]) sl_key = true;
            data['action_name'] = self.action_name;
            data['userName'] = self.userName;
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
        // 初始化筛选器
        sl_key: function (data) {
            // 初始化 返回列表
            return data
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
            var Url = self.Url + '/api/issus/';
            if(arguments.length === 2){
                Url = arguments[1];
            }

            data['pk'] = self.nid;
            data['action'] = "get_"+self.action;
            data['pk'] = self.nid;
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
                    }else{
                        self.items = resp.results;
                    }
                }
            );
        }
    }
});


var mydataPageVue = new MydataPageVue({
    ready: function () {
        this.loadData({});
    }
});

function MM_reload_mm(formId,statusId){
    var mydataPageVue = new MydataPageVue({
        ready: function () {
        }
    });
}