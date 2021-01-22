import requests
import io
import pandas as pd

# helper functions for building DataFrames
def build_df(url, decode = False, content_type = "", encoding = ""):
  """builds a DF from a url.

  Args:
      url (string): the URL
      decode (bool, optional): A boolean for whether the string needs to be decoded. Defaults to False.
      content_type (str, optional): The type of medium the URL will return. Defaults to "".
      encoding (str, optional): If encoding is needed. Defaults to "".

  Returns:
      [type]: [description]
  """      
    if url:
      request = requests.get(url)
    if request:
      data = request
      try:
        if content_type == 'json':
          df = pd.read_json(data.text)
        elif content_type == 'csv':
          df = pd.read_csv(data.text)
        return df
      except Exception as e:
        print(f"Exception creating the DF {e}")
        return pd.DataFrame()
    else:
        print(f"Error calling {url} {request.status_code}")
        return pd.DataFrame()

def github_helper(url, data_type):
  """Handles turning Github url into a dataframe.

  Args:
      url (string): the url.
      data_type (string): the content type of the returned data.

  Returns:
      Dataframe: A data frame.
  """    
    request = requests.get(url)
    if request:
      if data_type == 'csv':
          tmp_io = io.StringIO()
          tmp_io = io.StringIO(request.content.decode('utf-8'))
          return pd.read_csv(tmp_io)
      else :
        print(f"github request response ==> {request.status_code}")
        return pd.DataFrame()
    else :
      return pd.DataFrame()

# plot helpers
def forward(x):
  """A helper for scaling the y axis.

  Args:
      x (int): the number manipulate.

  Returns:
      int: the number to be used in scaling.
  """      
    return x ** (1 / 2)

def inverse(x):
  """A helper for scaling the y axis.

  Args:
      x (int): the number manipulate.

  Returns:
      int: the number to be used in scaling.
  """       
  return x ** 2

colors = ['#2678B2', '#AFC8E7', '#FD7F28', '#FDBB7D',
  '#339E34', '#9ADE8D', '#D42A2F', '#FD9898',
  '#9369BB', '#C5B1D4', '#8B564C', '#C39C95',
  '#E179C1', '#F6B7D2', '#7F7F7F', '#C7C7C7']

len_color = len(colors)# %% codecell
lockown_url = " 'cases'"

# AWS helpers
def write_dataframe_to_parquet_on_s3(dataframe, s3_bucket, folder, filename, partition=""):
    """
    Writes a DF to S3
    Args:
        dataframe (DF): A DataFrame to write to s3.
        s3_bucket (str): The S3 buckett to write to.
        folder (str): the S3 folder to write to.
        filename (str): the file name.
        partition (str, optional): the parition column(s). Defaults to "".
    """    
    print("Writing {} records to {}".format(len(dataframe), filename))
    output_file = f"s3://{s3_bucket}/{folder}/{filename}.parquet"
    if not partition: 
        dataframe.to_parquet(output_file)
    else:
        dataframe.to_parquet(output_file, partition_cols=[partition])

# move to helpers
def run_query(cur, conn, queries, action=""):
    """
    Runs a list queries. An exception will be raised on all errors.
    Parameters:
    cur: a cursor object
    conn: a connection object
    queries: a list of queries
    action: a string that will be used in logging to show what action is happening
    """
    if not isinstance(queries, list):
        tmp = list()
        tmp.append(queries)
        queries = tmp
    try:
        for query in queries:
            print("Starting {}".format(query))
            cur.execute(query)
            conn.commit()
            print(f"Commit completed")
    except Exception as e:
        print("Error on {}: {}".format(action, e))  
        cur.execute("ROLLBACK;")

def copy_to_rs(table, from_path, format, role):  
  """Builds a copy command.
  Args:
      table (str): the table name to copy into.
      from_path (str): the s3 path.
      format (str): the format of the s3 file.
      role (str): the AWS role to use.

  Returns:
      [type]: [description]
  """      

    if format == 'parquet':
        region = ""
    else:
        region = f"'us-east-1'"
    copy_command = (f"""
    COPY {table} FROM '{from_path}'
    credentials 'aws_iam_role={role}'
        {region}
        format as {format}
        COMPUPDATE OFF 
        STATUPDATE OFF;
    """)
    return copy_command

def check_s3_write(s3, s3_bucket, folder , filename, file_type):
  """Checks if an s3 file exists.

  Args:
      s3 (s3fs): an s3fs object.
      s3_bucket (str): the s3 bucket.
      folder (str): the s3 folder.
      filename (str): the filename.
      file_type (str): the type of the file.

  Returns:
      Bool: A boolean based on if the file was found.
  """    
    s3_path = f"{s3_bucket}/{folder}/{filename}.{file_type}"
    tmp = s3.ls(path=s3_path, detail=True, refresh=False)
    if tmp:
        print(f"tmp {tmp}")
        if tmp[0]['Key'] in s3_path:
            print("s3 file name match")
            return True
        else:
            print("NO s3 file name match")
            return False
    else:
        return False

def dq_query(cur, table):
  """Runs a data quality check query

  Args:
      cur (Psycopg cursor): The cursor.
      table (str): the table name

  Returns:
      tuple or Error: the tuple of results or an error.
  """    
    query = f"""
        SELECT COUNT(*) FROM {table}
    """
    try:
        cur.execute(query)
        return cur.fetchone()
    except Exception as e:
        err = e
        return err

def process_dq_results(results, table):
  """Processes the dq_query result.

  Args:
      results (tuple): the tuple of results.
      target (str): the table that was queried.
  """    
    if isinstance(results, tuple):
        if results[0] > 0:
            print(f"There are {results[0]} rows in {table}. Looks good.")
        else:
            print(f"There are {results[0]} rows in {table}. Please verify.")
    else:
        print(f"There was an error running the data check {results}")    