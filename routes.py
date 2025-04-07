from flask import Blueprint, request, jsonify, session, render_template
from models import db, Usuario, Rol, Material, Tina, Rollo, Tarjeta, Verificacion, RegistroCorte
from datetime import datetime

routes = Blueprint('routes', __name__)
# ============================
# DASHBOARDS POR ROL (HTML)
# ============================

@routes.route('/dashboard/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@routes.route('/dashboard/supervisor')
def supervisor_dashboard():
    return render_template('supervisor_dashboard.html')

@routes.route('/dashboard/calidad')
def calidad_dashboard():
    return render_template('calidad_dashboard.html')

@routes.route('/dashboard/cortador')
def cortador_dashboard():
    return render_template('cortador_dashboard.html')

# ============================
# AUTENTICACIÓN
# ============================

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    usuario = db.session.query(Usuario).filter_by(email=email, password=password).first()
    if usuario:
        session['usuario_email'] = usuario.email
        return jsonify({"msg": "Inicio de sesión exitoso", "rol": usuario.rol.nombre}), 200
    return jsonify({"msg": "Credenciales incorrectas"}), 401

@routes.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario_email', None)
    return jsonify({"msg": "Sesión cerrada"}), 200

# ============================
# VERIFICAR ROL
# ============================

def rol_requerido(*roles_permitidos):
    def decorator(f):
        def wrapper(*args, **kwargs):
            email = session.get('usuario_email')
            if not email:
                return jsonify({"msg": "No autenticado"}), 401
            usuario = db.session.query(Usuario).filter_by(email=email).first()
            if usuario and usuario.rol.nombre in roles_permitidos:
                return f(usuario, *args, **kwargs)
            return jsonify({"msg": "Acceso denegado: rol no autorizado"}), 403
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# ============================
# MATERIALES
# ============================

@routes.route('/materiales', methods=['GET'])
@rol_requerido('Administrador', 'Cortador', 'Calidad')
def obtener_materiales(usuario):
    materiales = db.session.query(Material).all()
    resultado = [{"id": m.id_material, "nombre": m.nombre} for m in materiales]
    return jsonify(resultado)

@routes.route('/materiales', methods=['POST'])
@rol_requerido('Administrador', 'Cortador')
def crear_material(usuario):
    data = request.get_json()
    try:
        nuevo = Material(nombre=data.get('nombre'), descripcion=data.get('descripcion'))
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"msg": "Material creado"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear material", "error": str(e)}), 500

# ============================
# TINAS
# ============================

@routes.route('/tinas', methods=['POST'])
@rol_requerido('Cortador')
def registrar_tina(usuario):
    data = request.get_json()
    try:
        nueva = Tina(
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            material_id=data.get('material_id'),
            usuario_id=usuario.id_usuario
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"msg": "Tina registrada"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al registrar tina", "error": str(e)}), 500

@routes.route('/tinas', methods=['GET'])
@rol_requerido('Administrador', 'Calidad')
def ver_tinas(usuario):
    tinas = db.session.query(Tina).all()
    resultado = [{"id": t.id_tina, "descripcion": t.descripcion, "fecha": str(t.fecha)} for t in tinas]
    return jsonify(resultado), 200

# ============================
# ROLLOS
# ============================

@routes.route('/rollos', methods=['POST'])
@rol_requerido('Cortador')
def registrar_rollo(usuario):
    data = request.get_json()
    try:
        nuevo = Rollo(
            descripcion=data.get('descripcion'),
            cantidad=data.get('cantidad'),
            fecha_uso=data.get('fecha_uso'),
            fecha_entrega=data.get('fecha_entrega'),
            material_id=data.get('material_id'),
            cortador_id=usuario.id_usuario
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"msg": "Rollo registrado"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al registrar rollo", "error": str(e)}), 500

@routes.route('/rollos', methods=['GET'])
@rol_requerido('Administrador', 'Calidad')
def ver_rollos(usuario):
    rollos = db.session.query(Rollo).all()
    resultado = [{
        "id": r.id_rollo,
        "descripcion": r.descripcion,
        "cantidad": float(r.cantidad),
        "fecha_uso": str(r.fecha_uso),
        "fecha_entrega": str(r.fecha_entrega),
        "material_id": r.material_id
    } for r in rollos]
    return jsonify(resultado), 200

# ============================
# TARJETAS
# ============================

@routes.route('/tarjetas', methods=['POST'])
@rol_requerido('Cortador')
def registrar_tarjeta(usuario):
    data = request.get_json()
    try:
        nueva = Tarjeta(
            tipo=data.get('tipo'),
            estado=data.get('estado'),
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            material_id=data.get('material_id'),
            tina_id=data.get('tina_id'),
            rollo_id=data.get('rollo_id'),
            usuario_id=usuario.id_usuario
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"msg": "Tarjeta registrada"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al registrar tarjeta", "error": str(e)}), 500

@routes.route('/tarjetas', methods=['GET'])
@rol_requerido('Administrador', 'Calidad')
def ver_tarjetas(usuario):
    tarjetas = db.session.query(Tarjeta).all()
    resultado = [{
        "id": t.id_tarjeta,
        "tipo": t.tipo,
        "estado": t.estado,
        "descripcion": t.descripcion,
        "fecha": str(t.fecha)
    } for t in tarjetas]
    return jsonify(resultado), 200

# ============================
# VERIFICACIONES
# ============================

@routes.route('/verificaciones', methods=['POST'])
@rol_requerido('Calidad')
def registrar_verificacion(usuario):
    data = request.get_json()
    try:
        nueva = Verificacion(
            tipo=data.get('tipo'),
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            usuario_id=usuario.id_usuario,
            material_id=data.get('material_id'),
            tina_id=data.get('tina_id')
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"msg": "Verificación registrada"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al registrar verificación", "error": str(e)}), 500

@routes.route('/verificaciones', methods=['GET'])
@rol_requerido('Administrador', 'Calidad')
def ver_verificaciones(usuario):
    verificaciones = db.session.query(Verificacion).all()
    resultado = [{
        "id": v.id_verificacion,
        "tipo": v.tipo,
        "descripcion": v.descripcion,
        "fecha": str(v.fecha)
    } for v in verificaciones]
    return jsonify(resultado), 200

# ============================
# REGISTROS DE CORTE
# ============================

@routes.route('/registros_corte', methods=['POST'])
@rol_requerido('Cortador')
def registrar_corte(usuario):
    data = request.get_json()
    try:
        nuevo = RegistroCorte(
            fecha=data.get('fecha'),
            descripcion=data.get('descripcion'),
            cortador_id=usuario.id_usuario,
            material_id=data.get('material_id')
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"msg": "Registro de corte guardado"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al registrar corte", "error": str(e)}), 500

@routes.route('/registros_corte', methods=['GET'])
@rol_requerido('Administrador', 'Calidad')
def ver_registros_corte(usuario):
    registros = db.session.query(RegistroCorte).all()
    resultado = [{
        "id": r.id_registro,
        "fecha": str(r.fecha),
        "descripcion": r.descripcion
    } for r in registros]
    return jsonify(resultado),200