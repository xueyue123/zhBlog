# zhBlog --一个Django框架开发的开源博客系统

1,名称：zhBlog系统， 我的博客: http://www.zhblog.cn

2,博客系统功能介绍:

	后台管理功能
    文章管理功能
    分类管理功能
	随笔管理功能
	评论功能
	留言功能
	相册管理功能
	友情链接管理功能
	用户设置功能（修改用户信息）
    站内搜索功能(根据关键字搜索站内文章)
	订阅功能
	收藏功能

3,博客模板介绍:

	1)前端采用"博客园"皮肤模板
	2)后台采用"豪情博客皮肤模板"
	理由:两套模板都非常简洁，小巧，干净，适合写技术文章或做笔记，记录等内容;
	缺陷:大众化，缺少修改内容;

4,博客使用技术介绍:

	1)Python语言,博客系统后台采用Python的Django框架开发,快速高效
	2)前端技术:Html,CSS,Javascript,jQuery
	3)部署:Nginx+uwsgi

5,使用说明

	安装mysql, 密码123456(如果改动请更改项目目录中的settings.py文件中的数据库密码)
	运行update.sh, ./update.sh,会创建数据库和创建测试数据；
	使用niginx+uwsgi部署,先启动nginx, sudo /usr/local/nginx/sbin/nginx, 再启动uwsgi, uwsgi --ini project.ini
	


