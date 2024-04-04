from db_utils import get_connection, create_scripts_table, insert_script_data
from scripts_utils import get_scripts  


def main():
    connection = get_connection()
    scripts = get_scripts()
    create_scripts_table(connection)
    insert_script_data(connection, scripts, batch_size=1000)

if __name__ == '__main__':
    main()