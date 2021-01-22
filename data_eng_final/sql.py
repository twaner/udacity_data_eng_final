import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('config.cfg')
SCHEMA = config.get('DB', 'SCHEMA')
IAM = config.get('IAM_ROLE', 'ARN2')

# Schema Management
set_schema = (f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")
set_search_path = (f"SET search_path TO {SCHEMA};")

# CREATE TABLES
states_table_create = (f""" 
CREATE TABLE IF NOT EXISTS {SCHEMA}.states (
    state_fips VARCHAR(4) NOT NULL PRIMARY KEY,
    state VARCHAR(40) NOT NULL,
    population BIGINT NOT NULL
    )
    diststyle all;
""")

county_table_create = (f""" 
CREATE TABLE IF NOT EXISTS {SCHEMA}.counties (
    county_fips VARCHAR(6) NOT NULL PRIMARY KEY,
    county VARCHAR(60) NOT NULL,
    state_fips VARCHAR(4) NOT NULL,
    population BIGINT NOT NULL
    )
    diststyle all;
""")

time_table_create = (f"""
CREATE TABLE IF NOT EXISTS {SCHEMA}.time (
date DATE NOT NULL PRIMARY KEY,
day BIGINT NOT NULL, 
week BIGINT NOT NULL, 
month BIGINT NOT NULL, 
year BIGINT NOT NULL, 
weekday BIGINT NOT NULL
)
diststyle all;
""")

state_covid_table_create = (f""" 
CREATE TABLE IF NOT EXISTS {SCHEMA}.state_covid (
    date Date NOT NULL,
    fips VARCHAR(3) NOT NULL,
    cases BIGINT NOT NULL,
    deaths BIGINT NOT NULL,
    cases_to_death DOUBLE PRECISION NOT NULL
    )
    diststyle all;
""")

county_covid_table_create = (f""" 
CREATE TABLE IF NOT EXISTS {SCHEMA}.county_covid (
    date Date NOT NULL,
    fips VARCHAR(5) NOT NULL,
    cases BIGINT NOT NULL,
    deaths BIGINT NOT NULL,
    cases_to_death DOUBLE PRECISION NOT NULL
    )
    diststyle all;
""")

# Table create list. This list will be used to set which tables get created.
tables_to_create = [states_table_create, county_table_create, time_table_create, state_covid_table_create, county_covid_table_create]
