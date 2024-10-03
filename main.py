from flask import Flask,jsonify
from extensions import db,jwt
from auth import auth_bp
from users import user_bp

def create_app():
    
    app = Flask(__name__)
    
    app.config.from_prefixed_env()
    
    #initialize exts
    db.init_app(app)
    jwt.init_app(app)

    #register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
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

