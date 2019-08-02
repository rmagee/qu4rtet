aws ssm put-parameter --name "/GENBIO-PROD/USE_AWS" --value "True" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/DJANGO_AWS_ACCESS_KEY_ID" --value "AKIA3Z6ACKM2DUXIXP4F" --type "SecureString"
aws ssm put-parameter --name "/GENBIO-PROD/DJANGO_AWS_SECRET_ACCESS_KEY" --value "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" --type "SecureString"
aws ssm put-parameter --name "/GENBIO-PROD/DJANGO_AWS_STORAGE_BUCKET_NAME" --value "qu4rtet.io.genbiopro-tasks" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/DATABASE_HOST" --value "qu4rtet-prod-cluster.cluster-cec4pnzwj4pp.us-east-1.rds.amazonaws.com" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/POSTGRES_DB" --value "qu4rtet" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/POSTGRES_USER" --value "qu4rtet" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/POSTGRES_PORT" --value "5432" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/POSTGRES_PASSWORD" --value "VGJ63qwhqGDwum3n5Dm6TXDUYr8YZWGu" --type "SecureString"
aws ssm put-parameter --name "/GENBIO-PROD/DJANGO_SECRET_KEY" --value "d#u))1)omq#&z(+(d_n=e3)hjs0_4nb$vr&-$7dn+8xswon*io" --type "SecureString"
aws ssm put-parameter --name "/GENBIO-PROD/DJANGO_DEBUG" --value "False" --type "String"
aws ssm put-parameter --name "/GENBIO-PROD/DJANGO_ENABLE_ADMIN" --value "True" --type "String"



psql -h qu4rtet-prod-cluster.cluster-cec4pnzwj4pp.us-east-1.rds.amazonaws.com -U qu4rtet





