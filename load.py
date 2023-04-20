import psycopg2
from config import dict_database_config

class LoadEstimatedTime:
    '''
    Crea la tabla suma_tiempo y agregar la sumatoria del tiempo estimado por tipo de producto, 
    primero se crea la tabla y luego se usa una consulta INSERT INTO ... SELECT para insertar 
    los datos calculados en la tabla suma_tiempo.
    '''

    connection = psycopg2.connect(user=dict_database_config['DB_USER'],
                                password=dict_database_config['DB_PASSWORD'],
                                host=dict_database_config['DB_HOST'],
                                port=dict_database_config['DB_PORT'],
                                database=dict_database_config['DB_NAME']
                                )

    cursor = connection.cursor()

    # Creating suma_tiempo table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suma_tiempo (
        id SERIAL PRIMARY KEY,
        producto INTEGER,
        tiempo_estimado_total DOUBLE PRECISION
    )
    ''')

    connection.commit()

    # Calculating the estimated time sum by product type and inserting it on suma_tiempo table
    cursor.execute('''
        INSERT INTO suma_tiempo (producto, tiempo_estimado_total)
        SELECT producto, SUM(time_estimate)
        FROM proyectos
        GROUP BY producto
    ''')

    connection.commit()

    cursor.close()
    connection.close()
