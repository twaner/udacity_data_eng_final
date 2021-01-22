# Udacity Data Engineering Project Final: Covid Data

## A look at Covid data at the statet and county level.

## Scoping the Project
### The data
The data is pulled from the New York Time's Github repository for their Covid numbers. We look at both the County and State level data. 

To supplement the State and County level Covid data, Census APIs are used to gather population numbers for each county and state.

## Purpose
The purpose of the model is to allow for an end user to combine Covid and population data in order to not only look at Covid rates, but to be able to break them down against a population of a given area.

## ETL Process Overview
The ETL process begins by creating the tables in Redshift. Once that is completed, then, one by one, each API is called and put into a Pandas Dataframe. Once in a DF, the data is engineered to meet the end standards.

An S3FS object is created in order to load files to S3.

Once the DF is in the desired format, the data is sent to S3, where it is stored as a parquet file.

After the file is loaded to S3, a data check is run in order to ensure that the file exists and the it is moved to Redshift.

## ETL Process Details
The ETL Process is as follows:
- Between each data frame being created, the data frame is uploaded to S3 in parquet format and the resulting file is copied to Redshift.

- Call the Census APIs in order to create county and state data frames. These data frames require data massaging in order to turn the Federal Information Processing Standards, FIPS code, into properly formattted strings. Two digit for states and three digit for countries. This requires casting Integers to strings and then padding and splitting them in order to ensure the same format across data frames.
- Upload the files to S3 in parquet format.
- Verify the files have been placed/exist in S3.
- Load to Redshift via COPY command.
- Run data checks.

## Data Dictionary
- Time Table

| Column | Description |
| ----------- | ----------- |
| date | DATE |
| day | DECIMAL |
| week | DECIMAL |
| month | DECIMAL |
| year | DECIMAL |
| weekday | DECIMAL |

- States Table

| Column | Description |
| ----------- | ----------- |
|state_fips | VARCHAR|
|state | VARCHAR|
|population | BIGINT|

- Counties Table

| Column | Description |
| ----------- | ----------- |
|county_fips|  VARCHAR|
|county | VARCHAR|
|state_fips | VARCHAR|
|population | BIGINT |

- State Covid Table

| Column | Description |
| ----------- | ----------- |
|date | Date|
|fips | VARCHAR|
|cases | BIGINT|
|deaths | BIGINT|
|cases_to_death | DOUBLE PRECISION|

- County Covid Table

| Column | Description |
| ----------- | ----------- |
|date | Date|
|fips | VARCHAR|
|cases | BIGINT|
|deaths | BIGINT|
|cases_to_death | DOUBLE PRECISION|

## Defending Decisions
Due to the nature of the data and its size, Pandas works well. As the data that is being requested grows in size, more customizations are done to it, or more tables are joined, a different tool, such as Spark, that allowed for scaling up resources would be more effective than running Pandas. This could be accomplished on AWS and allow for both those resources and the Redshift database resources to scale with demand of data processing and end users who would access the database.

In addition, due to the nature of the Covid data sets being updated daily, Airflow would be an apropriate choice. This would allow for the pipelines to run on a schedule to check for new data in the end sources and then run the ETL process to update the tables with new rows. That would require the