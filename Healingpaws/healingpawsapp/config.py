import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://healingpaws:4tYZ8NPRbi3j7JZM@healingpaws.top/healingpaws'
    # 123456
#mysql -u healingpaws -p4tYZ8NPRbi3j7JZM -h healingpaws.top -P 3306 -D healingpaws
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://healingpaws:4a47475b60356cbc@localhost:3306/healingpaws' #跑不了。。。。。。
    #这货是MySQL，不是SQLite hhh
    #所以肯定没有SQLALCHEMY
    #然后应该新开一个专门连MySQL的python文件，因为MySQL是上古时期的数据库，sqlite是最近才有哒
    # 我们是这么想的，当本地数据库创建好之后，将数据库放到云端的mysql的环境里变成MySQL的数据库
    #谁提出来的哇？
    # 有个组这么搞成功了。。。。。。
    #[飙泪笑]
    #不过，真的确定这样嘛
    #如果改成mysql的话，所有现在已有的数据库代码都要重写hhh
    #因为MySQL个SQLite就像微信和钉钉那种竞争关系
    #虽然我是微信这边的，但是钉钉也蛮好用的hhh
    #确定要改嘛
    # 是这样， 我们放上去的只是myapp。db这个文件
    # 每次写完更新myapp。db 然后把这个文件丢到mysql上

    #MySQL不兼容sqlite的任何东西hhh
    #这两家是竞争对手，MySQL是卖数据库赚钱哒，sqlite是一群程序员自己琢磨出来的
    #MySQL需要一个庞大的客户端，sqlite只需要很少的几行代码和一个.db的文件
    #MySQL的.db跟sqlite是不通哒
    # 那sqlite可以获得端口号、用户名和密码么
    #sqlite没有这些概念hhh，sqlite只有一个.db文件
    #端口，用户名还有密码那些是上古时期的MySQL才有的概念hhh
    # 那app 怎么连sqlite数据库
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydb.db')
    #这样就可以连sqlite啦
    # app 连数据库 不是flask连
    #也一样哒hhh
    #flask连完之后转出去哎
    #啥意思
    #flask连sqlite就这样写哇
    #这我知道，然后app怎么连到数据库
    #app是啥呀，安卓app还是flask app
    # 安卓app
    #不建议这么弄hhh，不过如果真的要搞的话嘛。。。
    #就这些啦
    # 他连的是mysql数据库
    # 这里是sqlite
    # 所以是设计错了
    #这样没法写的hhh
    #mysql和sqlite是竞争对手，用了某一家肯定是没法用另一家哒
    #行吧
    #所以不可能同时用俩哒，写完了sqlite代码之后移植到MySQL都很复杂hhh



    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CV_UPLOAD_DIR = os.path.join(basedir, 'uploaded_CV')

    # PHOTO_UPLOAD_DIR = os.path.join(basedir, 'uploaded_PHOTO')

    PHOTO_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_PHOTO')


