from diagrams import Cluster, Diagram
from diagrams.aws.analytics import EMR, Athena, Glue, Redshift
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.ml import Sagemaker
from diagrams.aws.storage import S3
from diagrams.generic.blank import Blank as Generic

with Diagram("AWS Data Lakehouse Architecture", show=False):
    with Cluster("Data Lake"):
        data_lake = S3("Data Lake")

    with Cluster("Data Warehouse"):
        data_warehouse = Redshift("Data Warehouse")

    with Cluster("Data Sources"):
        data_sources = [Dynamodb("DynamoDB"), Lambda("Lambda")]

    with Cluster("Data Processing"):
        data_processing = [Glue("Glue ETL"), EMR("EMR")]

    with Cluster("Data Analysis"):
        data_analysis = [Athena("Athena"), Sagemaker("SageMaker")]

    appflow = Generic("AppFlow")
    data_sources >> appflow >> data_lake
    data_lake >> data_processing
    data_processing >> data_warehouse
    data_warehouse >> data_analysis
