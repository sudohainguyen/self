from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudformation
from diagrams.aws.ml import Sagemaker
from diagrams.aws.storage import S3
from diagrams.generic.blank import Blank as Generic
from diagrams.onprem.vcs import Gitlab

with Diagram(
    "MLOps with GitLab and AWS SageMaker",
    show=False,
    filename="mlops-sagemaker/mlops-workflow",
):
    with Cluster("Development"):
        gitlab = Gitlab("GitLab")
        developer = Generic("Developer")

    with Cluster("CI/CD Pipeline"):
        pipeline = Generic("Pipeline")

    with Cluster("AWS SageMaker"):
        preprocessing = Sagemaker("Data Preprocessing")
        training = Sagemaker("Model Training")
        evaluation = Sagemaker("Model Evaluation")
        model = Sagemaker("Model")
        endpoint = Sagemaker("Endpoint")
        registry = Sagemaker("Model Registry")

    with Cluster("Data"):
        data = S3("Data")

    with Cluster("AWS Services"):
        lambda_func = Lambda("Lambda")
        eventbridge = Eventbridge("EventBridge")
        cloudformation = Cloudformation("CloudFormation")

    developer >> gitlab >> pipeline
    (
        pipeline
        >> preprocessing
        >> training
        >> evaluation
        >> model
        >> registry
        >> lambda_func
        >> cloudformation
        >> endpoint
    )
    data >> preprocessing
    registry >> eventbridge >> lambda_func
