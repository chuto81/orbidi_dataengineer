from config import dict_list_id
from extract import ExtractFromAPI
from build_database import BuildPostgreSQLDatabase
from transform import TransformProductNametoCode, TransformNumtoFloat
from load import LoadEstimatedTime


if __name__ == '__main__':

    # Extract all four JSON's list from ClickUp API and storing on dict
    dict_entities = {}
    for key, value in dict_list_id.items():
        instance_extract = ExtractFromAPI(key, value)
        instance_extract.api_request_get_clickup()
        dict_entities[key] = instance_extract.data_obtained()

    # Building lists for 'clientes' and 'proyectos'
    clientes_list = dict_entities['clientes']['tasks']
    proyectos_list = [task for key, value in dict_entities.items() if key != 'clientes' for task in value['tasks']]

    # Create the PostgreSQL database
    build_database = BuildPostgreSQLDatabase(clientes_list, proyectos_list)
    build_database.create_tables()
    build_database.insert_data()

    # Transform the PostgreSQL database
    transform_database1 = TransformProductNametoCode(proyectos_list)
    transform_database1.add_column()
    transform_database1.change_name_to_code()

    transform_database2 = TransformNumtoFloat()
    transform_database2()

    load_sum_estimated_time = LoadEstimatedTime()
    load_sum_estimated_time()

