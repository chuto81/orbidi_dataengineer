import psycopg2
from config import dict_database_config

class TransformProductNametoCode:
    '''
    Primero, se agrega una columna adicional llamada producto en la tabla proyectos y 
    luego se actualizan sus valores en función de las reglas dadas.
    
    Se agrega una columna producto a la tabla proyectos y utiliza la función get_producto_codigo 
    para transformar el nombre del proyecto en un código de producto. Al insertar proyectos en 
    la tabla, también se inserta el código del producto correspondiente en la columna producto. 
    Si el proyecto ya está en la tabla, la cláusula ON CONFLICT (external_id) DO UPDATE SET 
    producto = %s actualizará el valor del producto según el nombre del proyecto.
    '''

    connection = psycopg2.connect(user=dict_database_config['DB_USER'],
                                password=dict_database_config['DB_PASSWORD'],
                                host=dict_database_config['DB_HOST'],
                                port=dict_database_config['DB_PORT'],
                                database=dict_database_config['DB_NAME']
                                )
    
    def __init__(self, proyectos):
        self.proyectos = proyectos

    def add_column(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            ALTER TABLE proyectos
            ADD COLUMN IF NOT EXISTS producto INTEGER
            ''')
        self.connection.commit()

    # Method to change the product name to a numerical code
    def get_product_code(self, product_name):
        if 'KD-WEB' in product_name:
            return 0
        elif 'KD-SEO' in product_name:
            return 1
        elif 'KD-ANALITICA' in product_name:
            return 2
        elif 'KD-RRSS' in product_name:
            return 3
        elif 'KD-ECOMMERCE' in product_name:
            return 4
        elif 'KD-CRM' in product_name:
            return 5
        elif 'KD-PROC' in product_name:
            return 6
        elif 'KD-FACT' in product_name:
            return 7
        else:
            return None

    def change_name_to_code(self):
        cursor = self.connection.cursor()
        for proyecto in self.proyectos:
            producto_codigo = self.get_product_code(proyecto['name'])
            cursor.execute('''
            INSERT INTO proyectos (external_id, custom_id, name, text_content, description, 
            status_status, status_color, status_type, status_orderindex, orderindex, 
            date_created, date_updated, time_estimate, team_id, space_id, producto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (external_id) DO UPDATE SET producto = %s
            ''', (proyecto['id'], proyecto['custom_id'], proyecto['name'], proyecto['text_content'], 
                  proyecto['description'], proyecto['status']['status'], proyecto['status']['color'], 
                  proyecto['status']['type'], proyecto['status']['orderindex'], proyecto['orderindex'], 
                  proyecto['date_created'], proyecto['date_updated'], proyecto['time_estimate'], 
                  proyecto['team_id'], proyecto['space']['id'], producto_codigo, producto_codigo))
            self.connection.commit()

        cursor.close()
        self.connection.close()


class TransformNumtoFloat:
    '''
    Se cambian los campos numéricos a tipo double precision en las tablas clientes, proyectos 
    y cliente_proyecto. Se usa la sentencia ALTER TABLE para modificar las tablas existentes 
    y cambiar el tipo de dato de las columnas sin crear las tablas nuevamente.

    Se utiliza la sentencia ALTER TABLE para cambiar el tipo de dato de las columnas numéricas 
    en las tablas clientes, proyectos y cliente_proyecto a double precision. Tener en cuenta 
    que si se tienen datos existentes en estas tablas, es posible que se produzca una pérdida 
    de precisión al cambiar el tipo de dato a double precision.
    '''

    connection = psycopg2.connect(user=dict_database_config['DB_USER'],
                                password=dict_database_config['DB_PASSWORD'],
                                host=dict_database_config['DB_HOST'],
                                port=dict_database_config['DB_PORT'],
                                database=dict_database_config['DB_NAME']
                                )

    cursor = connection.cursor()

    # Change the data type from numerical to double precision
    cursor.execute('''
        ALTER TABLE clientes
        ALTER COLUMN status_orderindex TYPE DOUBLE PRECISION,
        ALTER COLUMN orderindex TYPE DOUBLE PRECISION,
        ALTER COLUMN date_created TYPE DOUBLE PRECISION,
        ALTER COLUMN date_updated TYPE DOUBLE PRECISION,
        ALTER COLUMN time_estimate TYPE DOUBLE PRECISION
    ''')

    cursor.execute('''
        ALTER TABLE proyectos
        ALTER COLUMN status_orderindex TYPE DOUBLE PRECISION,
        ALTER COLUMN orderindex TYPE DOUBLE PRECISION,
        ALTER COLUMN date_created TYPE DOUBLE PRECISION,
        ALTER COLUMN date_updated TYPE DOUBLE PRECISION,
        ALTER COLUMN time_estimate TYPE DOUBLE PRECISION
    ''')

    cursor.execute('''
        ALTER TABLE cliente_proyecto
        ALTER COLUMN date_created TYPE DOUBLE PRECISION
    ''')

    connection.commit()

    cursor.close()
    connection.close()
