# OldBoyCRM

# 请优先查看 install 文件夹下 内容.
手工创建文件夹 logs
## 安装顺序
### 生产环境
pip install -r ./install/requirement/commd.txt
###开发环境
pip install -r ./install/requirement/dev.txt
## pychram 配置
不建议直接配置生产环境.请使用dev环境配置.进行相关操作.
dev 环境配置时.请修改

#本次修改内容很多.请各位一定要做好相应测试.
1.增加 adminlte 模块 用于基础环境.主要包括模板.与一些系统层插件.
2.改变crm 位置. 变成可配置模块.
3.crm 增加 web_api api调用方法.里面有全套内容模板.
4.crm 增加 wen_models 原始 models 调用方法.此处需要大王验证 与原有功能是否一致.
5.crm 增加 web_views 用于存储crm web模板相关 主要负责前端调用.

# 查看文档顺序.
crm>web_views>crm_customer 前端调用相关
crm>web_api>issus>crm_customer API接口层

#其他
此次为临时 api 展现.具体的调用 需要周二晚上才能出来.


测试顺序.
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser #建立账户
python manage.py loaddata ./install/data/install.json # 菜单等
# 最后 在后台 建立
http://127.0.0.1:8080/admin/crm/customer/
客户信息中建立模拟数据.
目前 在导出 crm 总表时.有失败问题.次问题正在排查.

