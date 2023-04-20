import psycopg2
from config import dict_database_config


class BuildPostgreSQLDatabase:
    '''
    Esta clase crea una tabla separada cliente_proyecto para almacenar las relaciones
    entre clientes y proyectos basadas en 'linked_tasks'. Después de insertar clientes
    y proyectos en sus respectivas tablas, el script inserta las relaciones en la tabla
    cliente_proyecto utilizando los ID internos de las tablas clientes y proyectos.

    No se tomó en cuenta todos los datos de clientes y proyectos, porque implica la
    creación de otras multiples tablas, para seguir los principios ACID de bases de datos
    relacionales SQL.
    '''

    connection = psycopg2.connect(user=dict_database_config['DB_USER'],
                                password=dict_database_config['DB_PASSWORD'],
                                host=dict_database_config['DB_HOST'],
                                port=dict_database_config['DB_PORT'],
                                database=dict_database_config['DB_NAME']
                                )

    def __init__(self, clientes, proyectos):
        self.clientes = clientes
        self.proyectos = proyectos

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            external_id VARCHAR(255) UNIQUE,
            custom_id VARCHAR(255),
            name VARCHAR(255),
            text_content TEXT,
            description TEXT,
            status_status VARCHAR(255),
            status_color VARCHAR(255),
            status_type VARCHAR(255),
            status_orderindex INTEGER,
            orderindex VARCHAR(255),
            date_created BIGINT,
            date_updated BIGINT,
            time_estimate INTEGER,
            team_id VARCHAR(255),
            space_id VARCHAR(255)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id SERIAL PRIMARY KEY,
            external_id VARCHAR(255) UNIQUE,
            custom_id VARCHAR(255),
            name VARCHAR(255),
            text_content TEXT,
            description TEXT,
            status_status VARCHAR(255),
            status_color VARCHAR(255),
            status_type VARCHAR(255),
            status_orderindex INTEGER,
            orderindex VARCHAR(255),
            date_created BIGINT,
            date_updated BIGINT,
            time_estimate INTEGER,
            team_id VARCHAR(255),
            space_id VARCHAR(255)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente_proyecto (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER,
            proyecto_id INTEGER,
            date_created BIGINT,
            userid INTEGER,
            workspace_id VARCHAR(255),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
        ''')

        self.connection.commit()
        cursor.close()

    def insert_data(self):
        cursor = self.connection.cursor()

        for cliente in self.clientes:
            cursor.execute('''
            INSERT INTO clientes (external_id, custom_id, name, text_content, 
            description, status_status, status_color, status_type, status_orderindex, 
            orderindex, date_created, date_updated, time_estimate, team_id, space_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (external_id) DO NOTHING
            ''', (cliente['id'], cliente['custom_id'], cliente['name'], cliente['text_content'], 
                  cliente['description'], cliente['status']['status'], cliente['status']['color'], 
                  cliente['status']['type'], cliente['status']['orderindex'], cliente['orderindex'], 
                  cliente['date_created'], cliente['date_updated'], cliente['time_estimate'], 
                  cliente['team_id'], cliente['space']['id']))
            self.connection.commit()


        for proyecto in self.proyectos:
            cursor.execute('''
            INSERT INTO proyectos (external_id, custom_id, name, text_content, description, 
            status_status, status_color, status_type, status_orderindex, orderindex, 
            date_created, date_updated, time_estimate, team_id, space_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (external_id) DO NOTHING
            ''', (proyecto['id'], proyecto['custom_id'], proyecto['name'], proyecto['text_content'], 
                  proyecto['description'], proyecto['status']['status'], proyecto['status']['color'], 
                  proyecto['status']['type'], proyecto['status']['orderindex'], proyecto['orderindex'], 
                  proyecto['date_created'], proyecto['date_updated'], proyecto['time_estimate'], 
                  proyecto['team_id'], proyecto['space']['id']))
            self.connection.commit()

        # Inserting the relationships cliente_proyecto on that table
        for cliente in self.clientes:
            for linked_task in cliente['linked_tasks']:
                # Obteinig internal client ID and its project
                cursor.execute('SELECT id FROM clientes WHERE external_id = %s', 
                               (linked_task['task_id'],))
                cliente_id = cursor.fetchone()[0]
                cursor.execute('SELECT id FROM proyectos WHERE external_id = %s', 
                               (linked_task['link_id'],))
                proyecto_id = cursor.fetchone()[0]

                # Inserting the relationshio on cliente_proyecto table
                cursor.execute('''
                INSERT INTO cliente_proyecto (cliente_id, proyecto_id, date_created, userid, 
                workspace_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                ''', (cliente_id, proyecto_id, linked_task['date_created'], linked_task['userid'], 
                      linked_task['workspace_id']))
                self.connection.commit()

        # Closgin cursor and connection
        cursor.close()
        self.connection.close()
