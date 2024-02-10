resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_additional_perms" {
  name        = "lambda_additional_permissions"
  description = "Additional permissions for Lambda function"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "s3:*",
        "Effect" : "Allow",
        "Resource" : "*"
      },
      {
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Effect" : "Allow",
        "Resource" : "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_additional_perms.arn
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "rust-lambda"
  description   = "Create an AWS Lambda in Rust with Terraform"
  runtime       = "provided.al2"
  architectures = ["arm64"]
  handler       = "bootstrap"
  memory_size   = 256

  create_package         = false
  local_existing_package = "../rust-lambda/target/lambda/rust-lambda/bootstrap.zip"

  attach_policy = true
  policy        = aws_iam_policy.lambda_additional_perms.arn
}
