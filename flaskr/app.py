from flaskr import create_app
from .modelos import db, ReglaMonitoreo, ReglaMonitoreoSchema
from flask_restful import Api
from .vistas import VistaReglaMonitoreo

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaReglaMonitoreo, '/reglasmonitoreo')

#prueba
with app.app_context():
    regla_schema = ReglaMonitoreoSchema()
    r = ReglaMonitoreo(
        nombreUbicacion='casa', 
        numerosTelefonoArray='[123456,789456]', 
        notificarNumerosTelefono=True,
        notificarPropietario=True, 
        notificarPolicia=False, 
        notificarBomberos=True, 
        notificarPrimerosAuxilios=False
    )
    r2 = ReglaMonitoreo(
        nombreUbicacion='casa2', 
        numerosTelefonoArray='[123456,789456]', 
        notificarNumerosTelefono=True,
        notificarPropietario=True, 
        notificarPolicia=False, 
        notificarBomberos=True, 
        notificarPrimerosAuxilios=False
    )

    db.session.add(r)
    db.session.add(r2)
    db.session.commit()
    print(ReglaMonitoreo.query.all())
    print('now json')
    print([regla_schema.dumps(regla) for regla in ReglaMonitoreo.query.all()])