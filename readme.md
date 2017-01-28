## CMDB运维系统。
1. 运行环境：**python2.7.13 Linux : Centos7 Django == 1.8.16**

2. 功能：
    * 实现对服务器上的应用具有远程管理的能力
    * CMDB资产管理
        1. 程序端端具有操作远程服务器功能（基于paramiko）
        2. 用户端具有采集功能(服务器指标检测，cpu数据等)
        3. 用户管理功能 (暂时只有展示)
        4. 日志检测功能 （未实现）
        5. api访问接口（数据访问调用）

3. 文件结构
    * CMDBWork ---- 项目主目录
    * Api      ---- Api apps (接口模块)
    * Service  ---- Service apps (服务器展示)
    * User     ---- User apps (用户管理模块)
    * Log      ---- Log apps (日志模块)
    * static   ---- 所有静态配置文件
    * template ---- HTML模板文件
    * readme.md---- 说明文档
    * getInfo.py -- 服务器数据采集（采集端运行）

4. 启动项目：
    采用Pycharm启动，或者项目文件夹下面运行 python manager.py runserver 8000
    输入：http://127.0.0.1:8000/index/ 提示用户未登录自动跳转登陆页面，需要登陆管理员账户。
    * 用户名：zqred12
    * 密码：1155665



