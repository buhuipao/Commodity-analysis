# 这是妹子的毕业设计，是一个类似于慢慢买, 盒子比价网的商品价格比较、可视化的小系统

### 项目的目录结构基本为:
```
├── README.md
├── app.py
├── configs.py
├── configs.pyc
├── forms.py
├── forms.pyc
├── mydict
├── plots.py
├── plots.pyc
├── proxy.py
├── search.py
├── search.pyc
├── spider
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── amazon.py
│   ├── amazon.pyc
│   ├── jd.py
│   └── jd.pyc
├── sql
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── db.py
│   └── db.pyc
├── static
│   ├── e_history.png
│   └── e_history_low.png
├── templates
│   ├── 404.html
│   ├── 500.html
│   ├── base.html
│   ├── index.html
│   ├── info.html
│   └── search.html
└── test
    ├── datetime.html
    └── plots.py
```

## 想让这个项目跑起来需要做一些准备
  首先你需要准备一个MongoDB数据库, 推荐使用Dokcer的mongo镜像直接装一个，于是需要先安装Docker, 详细
步骤参考Docker官方文档：<https://www.docker.com/get-docker></https://www.docker.com/get-docker>,
在正确安装Docker之后， 参考<https://hub.docker.com/_/mongo/>安装Mongo数据库,详细步骤如下:
```
sudo docker run -v .data:/data/db -p 27017:27017 --name mymongo -d mongo --auth    #以认证的模式启动一个mongo容器
sudo docker exec -it mymongo mongo admin          #进入容器执行初始化命令, 并创建goods数据库
sudo docker ps                #确保容器正确运行
>db
admin
>db.createUser(
  { user: 'buhuipao',
    pwd: 'some-hard-guess-password',
    roles: [
      {role: "userAdminAnyDatabase",
        db: "admin"
      }
    ]
   });
Successfully added user: {
    "user" : "buhuipao-admin",
    "roles" : [
        {
            "role" : "userAdminAnyDatabase",
            "db" : "admin"
        }
    ]
}
>use goods
>db.createUser(
  {
    user: "buhuipao",
    pwd: "some-hard-guess-password",
    roles: [ { role: "readWrite", db: "goods" }]
  }
)
```
  由于安装了大量了第三方库,  在准备好数据库之后，需要使用如下命令安装多个第三方库;
  ```
sudo pip install -r requirfile
  ```
  安装完之后，直接运行:` gunicorn -w  2 app:app `就可以在浏览器`http://127.0.0.1:5000`看见界面了
