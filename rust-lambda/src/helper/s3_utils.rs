use aws_config::{meta::region::RegionProviderChain, BehaviorVersion};
use aws_sdk_s3::Client as S3Client;
use polars::prelude::*;
use std::error::Error;

const BUCKET: &str = "rust-s3";
const OBJECT_KEY: &str = "foods1.csv";

pub async fn get_data_from_s3() -> Result<DataFrame, Box<dyn Error + Send + Sync>> {
    // Load AWS configuration and create an S3 client
    let region_provider = RegionProviderChain::default_provider().or_else("ap-southeast-2");
    let config = aws_config::defaults(BehaviorVersion::latest())
        .region(region_provider)
        .load()
        .await;
    let s3_client = S3Client::new(&config);

    // Fetch the CSV file from S3
    let get_obj_resp = s3_client
        .get_object()
        .bucket(BUCKET)
        .key(OBJECT_KEY)
        .send()
        .await?;

    // Stream the object data directly into a byte buffer
    let data = get_obj_resp.body.collect().await?;
    let bytes = data.into_bytes();

    // Convert the byte buffer to a string, assuming UTF-8 encoding for the CSV data
    let csv_str = String::from_utf8(bytes.to_vec())?;

    // Use Polars to read the CSV data from the string
    let df = CsvReader::new(std::io::Cursor::new(csv_str))
        .infer_schema(None)
        .finish()?;

    Ok(df)
}
