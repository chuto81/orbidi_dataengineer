import psycopg2
from config import dict_database_config


class BuildPostgreSQLDatabase():
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
        cursor.execute("""
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
        """)

        cursor.execute("""
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
        """)

        cursor.execute("""
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
        """)

        self.connection.commit()
        cursor.close()


    # def insert_data(self):
    #     cursor = self.connection.cursor()

    #     for cliente in clientes:
    #         cursor.execute('''INSERT INTO clientes (id, custom_id, name, text_content, description) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING''', 
    #             (cliente['id'], cliente['custom_id'], cliente['name'], cliente['text_content'], cliente['description']))

    #     for producto in proyectos:
    #         cursor.execute('''INSERT INTO proyectos (id, custom_id, name, text_content, description) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING''', 
    #             (producto['id'], producto['custom_id'], producto['name'], producto['text_content'], producto['description']))

    #     for cliente in clientes:
    #         for link in cliente['linked_tasks']:
    #             cursor.execute('''INSERT INTO cliente_producto (task_id, link_id) VALUES (%s, %s) ON CONFLICT DO NOTHING''', 
    #                 (link['task_id'], link['link_id']))

    #     self.connection.commit()
    #     cursor.close()

    # def main():
    #     # self.connection = psycopg2.connect(user="your_user",
    #     #                             password="your_password",
    #     #                             host="127.0.0.1",
    #     #                             port="5432",
    #     #                             database="your_database")


    #     self.connection.close()

# if __name__ == "__main__":
#     main()
