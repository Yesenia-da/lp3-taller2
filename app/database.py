"""
Configuración de la base de datos y gestión de sesiones.
Utiliza SQLModel para ORM y gestión de conexiones.
"""

from sqlmodel import SQLModel, create_engine, Session, select
from typing import Generator
from sqlalchemy import text

from app.config import settings
# TODO: Crear el engine de la base de datos
# El engine es la conexión principal a la base de datos
# connect_args es específico para SQLite, remover para otras bases de datos
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Muestra las consultas SQL en consola si debug=True
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)


# TODO: Función para crear todas las tablas
def create_db_and_tables():
    """
    Crea todas las tablas en la base de datos.
    Se llama al iniciar la aplicación.
    """
    from app.models import Usuario, Pelicula, Favorito
    
    SQLModel.metadata.create_all(engine)
    print("Tablas de la base de datos creadas correctamente")


# TODO: Función para eliminar todas las tablas (útil para testing)
def drop_db_and_tables():
    """
    Elimina todas las tablas de la base de datos.
    Usar con precaución - elimina todos los datos.
    """
    SQLModel.metadata.drop_all(engine)
    print("Tablas de la base de datos eliminadas")


# Obtener una sesión de base de datos
def get_session() -> Generator[Session, None, None]:
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    
    Uso en endpoints:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session


# TODO: Opcional - Función para verificar la conexión a la base de datos
def check_database_connection() -> bool:
    """
    Verifica que la conexión a la base de datos funcione correctamente.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return False


# TODO: Opcional - Context manager para transacciones
class DatabaseSession:
    """
    Context manager para manejar sesiones de base de datos.
    Útil para operaciones fuera de endpoints FastAPI.
    
    Uso:
        with DatabaseSession() as session:
            user = session.get(Usuario, user_id)
    """
    def __enter__(self) -> Session:
        self.session = Session(engine)
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()


# TODO: Opcional - Función para inicializar datos de prueba
def init_sample_data():
    """
    Inicializa la base de datos con datos de prueba.
    Útil para desarrollo y testing.
    """
    from app.models import Usuario, Pelicula, Favorito

    with Session(engine) as session:
        # Evitar duplicar datos si la base de datos ya tiene información
        if (
            session.exec(select(Usuario)).first()
            or session.exec(select(Pelicula)).first()
            or session.exec(select(Favorito)).first()
        ):
            print("La base de datos ya contiene datos de prueba")
            return

        usuarios = [
            Usuario(nombre="Ana", correo="ana@example.com"),
            Usuario(nombre="Carlos", correo="carlos@example.com"),
            Usuario(nombre="Laura", correo="laura@example.com"),
        ]

        peliculas = [
            Pelicula(
                titulo="Interestelar",
                director="Christopher Nolan",
                genero="Ciencia ficción",
                duracion=169,
                año=2014,
                clasificacion="PG-13",
            ),
            Pelicula(
                titulo="Titanic",
                director="James Cameron",
                genero="Romance",
                duracion=195,
                año=1997,
                clasificacion="PG-13",
            ),
            Pelicula(
                titulo="Coco",
                director="Lee Unkrich",
                genero="Animación",
                duracion=105,
                año=2017,
                clasificacion="PG",
            ),
        ]

        session.add_all(usuarios)
        session.add_all(peliculas)
        session.commit()

        favoritos = [
            Favorito(id_usuario=usuarios[0].id, id_pelicula=peliculas[0].id),
            Favorito(id_usuario=usuarios[1].id, id_pelicula=peliculas[1].id),
            Favorito(id_usuario=usuarios[2].id, id_pelicula=peliculas[2].id),
        ]

        session.add_all(favoritos)
        session.commit()

        print("Datos de prueba inicializados correctamente")