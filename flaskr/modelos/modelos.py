from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
import enum
from werkzeug.security import check_password_hash, generate_password_hash

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

albumes_canciones = db.Table('album_cancion', \
   db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True), \
   db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    albumes = db.relationship('Album', secondary = 'album_cancion', back_populates = "canciones")

class Medio(enum.Enum):
    DISCO = 1
    CASETE = 2
    CD = 3

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio), nullable = False)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates = "albumes")
    __table_args__ = (db.UniqueConstraint('usuario', 'titulo', name = 'titulo_unico_album'),)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    # contrasena = db.Column(db.String(50))
    contrasena_hash = db.Column(db.String(255))
    albumes = db.relationship('Album', cascade = 'all, delete, delete-orphan')

    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible")
    
    @contrasena.setter
    def contrasena(self, password):
        self.contrasena_hash = generate_password_hash(password)
    
    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password)  

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}
    
class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cancion
        include_relationships = True
        load_instance = True

class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute = ("medio"))
    class Meta:
        model = Album
        include_relationships = True
        load_instance = True
    
class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

