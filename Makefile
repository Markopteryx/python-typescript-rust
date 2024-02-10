.PHONY: build-rust-lambda apply-terraform deploy

# Build the Rust Lambda function
build-rust-lambda:
	cd rust-lambda && cargo lambda build --release --arm64 --output-format zip

# Apply Terraform configuration
apply-terraform:
	cd infra && terraform apply --auto-approve

# Deploy command that builds and applies Terraform
deploy: build-rust-lambda apply-terraform