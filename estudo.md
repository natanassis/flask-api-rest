#  Jwt Autentication fro Flask-Jwt-Extended 

[Link do turtorial no youtube](https://youtu.be/aX-ayOb_Aho?si=_YVISFWwr4CryXzi)


Vamos inicar nosso projeto 
    
* Crie uma pasta para o projeto e coloque
    1. crie um virtualenv

            python -m venv env

    2. crie um arquivo dotenv chamado 
            
            .env
    3. Vamos instalar a biblioteca do flask e do dotenv

            $ pip install flask

        ---------------

            $ pip install python-dotenv


    4. Vamos criar um arquivo main.py
    
        1. vamos importa o flask e instancia o Objeto

                from flask import Flask

                def create_app():

                    app = Flask(__name__)

                    return app
    5. Vamos fazer as configurações para o arquivo .env
        * Dentro da função creat_app declare

                app.config.from_prefixed_env    

        * Dentro o arquivo .en coloque 

                FLASK_SECRET_KEY= CHAVE API
                FLASK_DEBUG=True
                FLASK_APP=main.py


-----
### Trabalhando com ORM

* Vamos Instalar a biblioteca Python para ORM

        $ pip install flask-sqlalchemy

* Vamos criar um arquivo chamado extensions para todas as nossas extensões

        > extensions.py

    * Dentro arquivo extensions digite 

            from flask_sqlalchemy import SqlAlchemy

            db = SqlAlchemy()

    * No arquivo .env digite as configurações que iram por App

            FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite
            FLASK_SQLALCHEMY_ECHO=True 

    * Dentro do arquivo App import o extension e coloque o db 

            from extension import db

            ***
            db.init_app(app)


* Criando as tabelas para o Database

    1. Crie um arquivo chamado **models.py** e nele vamos criar uma classe para represenatr a classe usario no database

            from extensions import db

            class User(db.Model):

                __tablename__ = 'users'
                id = db.Column(sb.String(), primary_key=True, defalt =str())

        ---
        * Criamos o id como **String** porque iremos usar uma biblioteca que cria id unicos a lib **uuid**

                from uuid import uuid4 
                ***

                id = db.Column(sb.String(), primary_key=True, defalt =str(uuid4()))

        * Vamos termina de criar a tabela de usuario 

                class User(db.Model):
                    __tablename__ = 'users'
                    id=db.Column(db.String(), primary_key=True, defalt =str(uuid4()))
                    username = db.Column(db.String(),nullable=False)
                    emials = db.Column(db.String(),nullable=False)
                    password(db.Column(db.Text,nullable=False)

                    def __repr__(self):
                        return f"<User {self.username}>"

        * Agora no terminal iremos acessar ao flask shell

                $ flask shell

        * Vamos criar nossa tabela do Database na flask shell

                $ db
            ----
                $ from models import User
            ---
                $ db.create_all() 


### Vamos criar nosso BluePrint

* Para criar o blueprint vamos, precisa criar um arquivo chamado **auth.py** e nele vamos fazer:

            from flask import Blueprint,jsonify


            auth_bp = Blueprint('auth',__name__)

            @auth_bp.post('/register')
            def register_user():
                return jsonify({"message":"created new user"})

* Dentro do arquivo main.py coloque a linha e import a auth que acabamso de criar 

            from auth impot auth_bp

            ***

            app.register_blueprint(auth_bp,url_prefix='/auth')

* Vamos organizar nossa classe user em models para receber novos usarios, deletar usuarios, comparar a senha e outras coisas:

        * No arquivo models digite:

                from werkzeug.security import generate_password_hash,check_password_hash 


                *** 
**Dentro a classe User digite**

----
*  Criando as classes que  fornece funções para lidar com segurança de senhas. 
----
                #A função generate_password_hash utiliza um algoritmo de hash com sal (salt) para gerar o hash da senha
                def set_password(self,password):
                        self.password = generate_password_hash(password)
----
                #  Verifica se uma senha fornecida corresponde ao hash armazenado.
                def check_password(self,password):
                        return check_password_hash(self.password,password)

                
Criando as funções de add e remove na class user,e o metodo de classe 

                 @classmethod    
                def get_user_by_username(cls,username):
                        return cls.query.filter_by(username=username).first()

                def add(self):
                        db.session.add(self)
                        db.session.commit()
                
                def remove(self):
                        db.session.remove(self)
                        db.session.commit()

#### Criando codigo para cadastrar user

* Dentro do arquivo **auth.py** vamos colocar a logica para criar o usuario 
        1.Dentro da função **register_user** digite:
---


                data = request.get_json()

                user =  User.get_user_by_username(username = data.get['username'])

                if user is not None:
                        return jsonify({"error": "user already exists"})

                new_user = User(
                        username = data.get['username'],
                        email = data.get['eamil]
                )

                // como colocamos uma segurança para senha vamos usar 
                new_user.set_password(password=data.get['password])

                // como criamos dois metodos para salvar e remover
                new_user.save()

                return jsonify({"message":User created"}), 201

### Criando ususario atraves do Json 

Para criar um usuario, acesse o postamn ou insominia 

* Criando usuario pelo api:
1. Para acessar a api usar a url abaixo:

        http://127.0.0.1:5000/
        
2. Para que seja cadastrado o usuario coloque essa link e faça um requisição POST:

        http://127.0.0.1:5000/auth/register

3. crie um **JSON** como mostrado abaixo:

        {
                "username":"caio",
                "email":"caio@gmail.com",
                "password":"123456"
        }

4. Se caso de tudo certo será retornado:

        {
                "message": "User created"
        }

5. Se caso o usuario for existente:

        {
                'error':"User already exists"
        }


### Trabalhando com Autenticação por JWT Token 

*  Antes de instalar a biblioteca para JWT Flask vamos criar um arquivo requirements.txt com todas as libs usadas:

        $ pip freeze > requirements.txt


* Para isso vamos intalar a lib que trabalha com JWT token no flask:

        $ pip install flask-jwt-extended

* Vamos configurar uam chave de **JWT** para as requisições, para isso vamos no terminal python e digitar:
        
        $ python

        >>> import secrets
        >>> secrets.token_hex(12)
        'faef4a84f6a4f856a8f'

* Dentro do arquivo .env declare uma nova variavel de ambiente:

        FLASK_JWT_SECRET_KEY=aef4a84f6a4f856a8f

* Vamos integrar lib do jwt a nossa estrutra do arquivo **extensions**:

        from flask_jwt_extended import JWTManager

        ***

        jwt = JWTManager()

* Dentro do arquivo main.py import o jwt de **extensions** e coloque na def create_app os parametros:
        
        from extensions import db,jwt

        ***
        jwt.init_app(app)

* No arquivo auth vamos configurar o token jwt para vim quando foi feito o login 
    1. Import o flask_jwt_extended para ser usado  
        
    2.  Crie um novo decoreitor e uma def para ele chamados:

                @auth_bp.post('/login')
                def login_user():

    
    3. Dentro desse **def** digite as seguintes linhas abaixo:

                // variavel para pegar os dados pelo request
                data = request.get_json()

                // variavel para instanciar o Objeto User
                user = User.get_user_by_username(username=data.get('username'))

                // para checar se a senha está correta
                if user and (user.check_password(password= data.get('password'))):

                        //  para criar o tokens jwt de access e refresh 
                        acces_token = create_access_token(identity=user.username)
                        refresh_token = create_refresh_token(identity=user.username)
                        
                        // caso usuario encontado retorna um json com os tokens e status 200
                        return jsonify(
                        {
                                "message":"Logged in",
                                "tokens": {
                                "access":acces_token,
                                "refresh":refresh_token
                                }
                                }
                        ), 200

                // caso esteja incorreto será retornado um json de error com o status  400 
                return jsonify({"error":"invalide username"}),400

        4. Vamos testar o login pelo **postman**, dentro do postman crie um nova aba como **POST** e digite o link:

                http://127.0.0.1:5000/api/auth/login 
        
        5. Faça a requisição atraves de um json que nem o exemplo abaixo:

                {
                "username":"caio",
                "password":"123456"
                }
        
        * Caso esteja ok sera retornado um json com os tokes e o status 200:

                // Podemos vr que temos nosso token de acesso, e um token de atualização
                {
                        "message": "Logged in",
                        "tokens": {
                                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwOTkzMzgwOSwianRpIjoiYmIxYTNiMTYtNjI0NC00YzRhLWIxM2YtY2M5OWQzYjMzMWQ4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1haWxhIiwibmJmIjoxNzA5OTMzODA5LCJjc3JmIjoiNjJjOGJlYTQtMTAyYy00MzZmLTk1NzgtNDhhZWMxMmQ4MmE0IiwiZXhwIjoxNzA5OTM0NzA5fQ.NY8P1CbPOJ61yjrTBaCYv88uUJiDzg2cfYASN0hWjh8",
                                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwOTkzMzgwOSwianRpIjoiNTdmY2MzNDctYjA2Mi00MmExLWJmZTEtODNmOGY1NGQyNWJkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJtYWlsYSIsIm5iZiI6MTcwOTkzMzgwOSwiY3NyZiI6IjYyZmQ2OWM5LWQ0ODEtNDQ0ZS04ZWY4LTAxMmM2M2I5ODcyYSIsImV4cCI6MTcxMjUyNTgwOX0.PmKT8a_cDCly9ADzXUQRH9SdSvECoMI0sE6BBrBykEc"
                        }
                }
        
        * Se for erro será retornado assim 

                {
                    "error":"invalide username"
                }

Agora vamos proteger nossas funções que só poderam ser acessadas quando um usuario tiver um par de JWT:

* Então para fazer isso, o que faremos é implementar alguns tipos de endpoint que excutará algo e veremos 
como podemos prever isso.


1. Vamos instalar a lib 
       
                pip install marshmallow

2. vamos criar um novo arquivo chamado **schemas.py** para usar o  marshmallow

        > schemas.py

* Dentro do Arquivo schemas digite:

                from marshmallow import fields,Schema

                class UserSchema(Schema):
                        id = fields.String()
                        username = fields.String()
                        email = fields.String()

3. Vamos criar um novo arquivo chamado  **users.py** para as rotas e busca

        > users.py

* Dentro do arquivo digite:

        from flask import Blueprint,request,jsonify
        from flask_jwt_extended import jwt_required
        from models import User
        from schemas import UserSchema

        // nova Blueprint
        user_bp = Blueprint(
        'api/users',
        __name__
        )
        // rota que ira rotar todos os usuarios ou 1 
        @user_bp.get('/all')
        // só pode ser acessar por meio de token jwt 

        @jwt_required()// decoreitor para verificar se tem token de autenticação
        def get_all_users():

                // Indica a página especifica 
                page = request.args.get('page',default=1,type=int)
                
                // Especifica o número de itens por pagina
                per_page = request.args.get('per_page',default=3,type=int)
                

                users = User.query.paginate(
                        page = page,
                        per_page= per_page,
                )
                
                result = UserSchema().dump(users,many=True)
                
                // retorno se operação for ok 
                return jsonify(
                        {
                        "users":result
                        }
                ),200


* Vamos falar para que ser o **page** e **per_page**:
        
        
    * **page**: Indica a página especifica que você deseja visualizar
    * **per_page**: Especifica o número de itens por pagina ou resultados a serem exibdos por página

* vamos definir uma nova Blueprint no app, no arquivo `main.py` digite:

        ***
        #register blueprints
        app.register_blueprint(user_bp, url_prefix='/api/users')

* vamos testar as novas rotas pelo Postman

1. dentro o postman faça uma nova requisão de login 

        http://127.0.0.1:5000/api/auth/login 

2. Pege o token de acesso e coloque na proxima Aba na parte de:

        Authorization-> Type -> Bearer Token -> Token

* coloque o Token  de access em token de **Bearer Tokne -> Token**, e faça a requisão **GET**

        http://127.0.0.1:5000/api/users/all?page=1

* Depois teste o per_page:

        http://127.0.0.1:5000/api/users/all?page=1&per_page=5


## Erros relacionados à autenticação JWT(JSON Web Token) em um aplicativo web:

No arquivo `main.py` declare os seguintes verificações de erro JWT:

        *** 
        # jwt error handlers
        @jwt.expired_token_loader
        def expired_token_callback(jwt_haeader,jwt_data):
                return jsonify({"message": "Token has expired",
                                "error": "token_expired"})


        @jwt.invalid_token_loader
        def invalid_token_callback(error):
                return jsonify({"message": "Singnature verification falid",
                                "error": "invalide_token"})
        
        @jwt.unauthorized_loader
        def missing_token_callback():
                return jsonify({"message": "Request doest contain invalid token",
                                "error":"authorization_header"})

        return app
        
**1.**`expired_token_callback(jwt_header,jwt_data)`

* **Objetivo**: trata casos em que um token expirou.
* **Aciona quando**: Uma solicitação é feita com um JWT expirado.

* **Ações**:
    *  Retorna uma resposta JSON com uma mensagem indicado a expiração do token e um código de erro("token_expired")  
    * A reposta normalmente tem um código de status 401(não autorizado).

**2.**`invlaide_token_callback(error):`
* **Objetivo**: trata de casos em que um token inválido devido a problemas como assinatura ou fomrato incorreto;
* **Acionado quando**: Uma solicitação é feita com um JWT inválid.
* *Ações**:
    * Retonra uma repostya JSON com uma mensagem indicado falha na assinatuira e um codigo de erro('invalid_token').
    * Geramente tamb´me tem um código de status 401.

**3.**: `missing_token_callback():`
* **Objetivo**: trata de casos em que uma solicitação não possui um JWT obrigatorio.
* **Acionado quando**: Uma solicitação não inclui um JWT no cabeçalho de autorização.
* **Ações**:

    * Retonra um reposta JSON com uma mensagem indicando o token ausente e um código de erro("authorization_header").
    * Geralmente também tem um codigo de status 401.

**Pontos chave**:

* Essas funções provavelmente fazem parte de um middleware ou estrutura de autenticação JWT em um aplicativo da web.

* Eles ajudam a fornecer respostas informativas aos clientes quando ocorrem erros de autenticação, melhorando a experiência e a segurança do usuário.

* Eles são invocados automaticamente pela estrutura quando surgem as condições de erro correspondentes.
