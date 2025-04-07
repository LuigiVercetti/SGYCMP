from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, DECIMAL, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ========================
# ROLES Y PERMISOS
# ========================

class Rol(db.Model):
    __tablename__ = 'roles'

    id_rol = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)

    permisos = relationship("RolPermiso", back_populates="rol")
    usuarios = relationship("Usuario", back_populates="rol")

class Permiso(db.Model):
    __tablename__ = 'permisos'

    id_permiso = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)

    roles = relationship("RolPermiso", back_populates="permiso")

class RolPermiso(db.Model):
    __tablename__ = 'roles_permisos'

    id_rol = Column(Integer, ForeignKey("roles.id_rol", ondelete="CASCADE"), primary_key=True)
    id_permiso = Column(Integer, ForeignKey("permisos.id_permiso", ondelete="CASCADE"), primary_key=True)

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")

# ========================
# USUARIOS
# ========================

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contraseña = Column(Text, nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id_rol", ondelete="SET NULL"))

    rol = relationship("Rol", back_populates="usuarios")
    materiales = relationship("Material", back_populates="creador")
    tinas = relationship("Tina", back_populates="operario")
    rollos = relationship("Rollo", back_populates="cortador")
    tarjetas = relationship("Tarjeta", back_populates="usuario")
    verificaciones = relationship("Verificacion", back_populates="usuario")
    cortes = relationship("RegistroCorte", back_populates="cortador")
    reportes = relationship("ReporteCalidad", back_populates="usuario")

# ========================
# LINEAS
# ========================

class Linea(db.Model):
    __tablename__ = 'lineas'

    id_linea = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)

    materiales = relationship("Material", back_populates="linea")

# ========================
# MATERIALES
# ========================

class Material(db.Model):
    __tablename__ = 'materiales'

    id_material = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    referencia = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)
    apertura = Column(String(10), CheckConstraint("apertura IN ('abierto', 'cerrado')"))
    diametro = Column(DECIMAL(10, 2))
    longitud = Column(DECIMAL(10, 2))
    creado_por = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))
    fecha_creacion = Column(DateTime, default=func.now())
    linea_id = Column(Integer, ForeignKey("lineas.id_linea", ondelete="SET NULL"))

    creador = relationship("Usuario", back_populates="materiales")
    linea = relationship("Linea", back_populates="materiales")
    tinas = relationship("Tina", back_populates="material")
    rollos = relationship("Rollo", back_populates="material")
    tarjetas = relationship("Tarjeta", back_populates="material")
    verificaciones = relationship("Verificacion", back_populates="material")
    cortes = relationship("RegistroCorte", back_populates="material")

# ========================
# TINAS
# ========================

class Tina(db.Model):
    __tablename__ = 'tinas'

    id_tina = Column(Integer, primary_key=True)
    tipo = Column(String(20), CheckConstraint("tipo IN ('pequeña', 'grande')"))
    estado = Column(String(20), CheckConstraint("estado IN ('llena', 'vacía')"))
    fecha = Column(Date, nullable=False)
    material_id = Column(Integer, ForeignKey("materiales.id_material", ondelete="SET NULL"))
    operario_id = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))

    material = relationship("Material", back_populates="tinas")
    operario = relationship("Usuario", back_populates="tinas")
    tarjetas = relationship("Tarjeta", back_populates="tina")
    verificaciones = relationship("Verificacion", back_populates="tina")

# ========================
# ROLLOS
# ========================

class Rollo(db.Model):
    __tablename__ = 'rollos'

    id_rollo = Column(Integer, primary_key=True)
    descripcion = Column(Text)
    cantidad = Column(DECIMAL(10, 2))
    fecha_uso = Column(Date, nullable=False)
    fecha_entrega = Column(Date, nullable=False)
    material_id = Column(Integer, ForeignKey("materiales.id_material", ondelete="SET NULL"))
    cortador_id = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))

    material = relationship("Material", back_populates="rollos")
    cortador = relationship("Usuario", back_populates="rollos")
    tarjetas = relationship("Tarjeta", back_populates="rollo")

# ========================
# TARJETAS
# ========================

class Tarjeta(db.Model):
    __tablename__ = 'tarjetas'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)    

class Verificacion(db.Model):
    __tablename__ = 'verificaciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materiales.id'), nullable=False)
    resultado = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class RegistroCorte(db.Model):
    __tablename__ = 'registros_corte'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materiales.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
