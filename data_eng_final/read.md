# Udacity Data Engineering Final

## Sumamry
The project pull in Covid data at the state and county level as well as census info at the same level. It creates data frames and normalizes all fields, stages them in S3, and then loads those files into Redshift.

## To Run
Download all required packages noted by the imports. Once that has been completed, add the required credentials to the .cfg file. Ensure that the S3 bucket and Redshift are reachable via tthe credentials.

With those steps completed the Jupyter notebook can be run to create the tables, create the data frames, pass the files into S3, and finally load to Redshift.

Data quality checks are run to ensure the files exist on S3 and SQL queries are used to ensure that the load to Redshift was successful.

Queries can be configured to pull data by date, county, state, or any other available criteria. Those queries can be run through helper functions and send to a matplotlib helper function to plot.

