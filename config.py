import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This class sets up the configuration for the Flask server"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a*HAiGjgNR9bd7Ex!!ejC&D*SLCEtzU3KJ%qeZ8UQWyWQT'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_NAME = os.environ["DB_NAME"]
    DB_SOCKET_DIR = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    CLOUD_SQL_CONNECTION_NAME = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False




pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        database=db_name,  # e.g. "my-database-name"
        query={
            "unix_socket": "{}/{}".format(
                db_socket_dir,  # e.g. "/cloudsql"
                cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
        }
    ),
    **db_config
)
