# createDynamoTable.sh
# APM Comics Demo
# Austin Krauza- June 2018
# Creates DynamoDB Table from the input schema JSON
aws dynamodb create-table --table-name "apm-comics-prod" --cli-input-json file://schema.json