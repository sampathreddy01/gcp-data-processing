runner="DataFlowRunner"  
tempbucket="gs://settetesttransferdata/tmp"
dataflow_staging="gs://settetesttransferdata/Staging/"
region='us-central1'
jobname='titanicdemo'
template_location="gs://settetesttransferdata/template_folder/template"
setup="/home/sette/toPostgreSQL/BQtoPostgreSQL/setup.py"
#input pattern
projectid='datalab-336505' 
sourcetablename="demodata"
tableid= "Titanic"  
#output pattern
target_tableid="target"
#Source config
drivername="postgresql+pg8000" 
host="35.239.104.9"
port="5432"
database="demodb"
username="postgres"
password="cvsgcp01"
create_if_missing="True"
# ./cloud_sql_proxy -instances==postgres tcp:5432


  

