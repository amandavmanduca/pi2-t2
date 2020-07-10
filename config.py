class config:
#    SQLALCHEMY_DATABASE_URI = 'mysql://fernandoiepsen:senac2020PI2@fernandoiepsen.mysql.pythonanywhere-services.com/fernandoiepsen$default'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/trabalho2_pi2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SALT = "X#3jfk$%kKmGw&*jKLiPW@!jm345"
    JWT_SECRET_KEY = 'hjsdfhj#$@DFhsms@%ldkPç()H#Dnx3@'
    JWT_BLACKLIST_ENABLED = True