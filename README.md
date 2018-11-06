### Flask框架实践

Flask + Bootstrap + MongoDB + Gunicorn + Nginx

部署于套路云[地址](http://39.105.187.104)

![](https://github.com/EddieIvan01/Flask_BBS/blob/master/demo_img/1.png)

![](https://github.com/EddieIvan01/Flask_BBS/blob/master/demo_img/2.png)

- [x] 发帖
- [x] 评论
- [x] 数据库分页
- [x] 头像等个人资料
- [x] Markdown编辑，用的Editor.md组件
- [x] 权限控制, (anonymous, basic, root)
- [ ] 关注，点赞
- [ ] RSS, 打算以后有时间用Golang写个API

踩坑无数，也学到了不少，具体见[Blog](http://iv4n.xyz/flask-bbs)

部署：

```
安装MongoDB并配置
安装Nginx并配置
安装Gunicorn
运行 bash run.sh
```
