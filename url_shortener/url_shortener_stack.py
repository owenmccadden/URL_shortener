from aws_cdk import core as cdk
from aws_cdk import aws_dynamodb, aws_lambda, aws_apigateway

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class UrlShortenerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        table = aws_dynamodb.Table(self, "mapping-table",
                                   partition_key=aws_dynamodb.Attribute(name='id',
                                                                        type=aws_dynamodb.AttributeType.STRING))

        function = aws_lambda.Function(self, "backend", runtime=aws_lambda.Runtime.PYTHON_3_8,
                                       handler="handler.main", code=aws_lambda.Code.asset("./lambda"))

        table.grant_read_write_data(function)  # permits lambda function to read and write to DynamoDB table
        function.add_environment('TABLE_NAME', table.table_name)  # sets table name environment variable for function

        api = aws_apigateway.LambdaRestApi(self, "api", handler=function)
