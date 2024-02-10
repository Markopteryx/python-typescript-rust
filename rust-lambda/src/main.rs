pub mod helper;

use crate::helper::s3_utils::get_data_from_s3;
use lambda_runtime::{run, service_fn, Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use tracing_subscriber::filter::{EnvFilter, LevelFilter};

#[derive(Deserialize)]
struct Request {
    message: String,
}

#[derive(Serialize)]
struct Response {
    req_id: String,
    msg: String,
}

fn say_hello(name: Option<&str>) -> String {
    let name = name.unwrap_or("world");
    format!("Hello, {name}!")
}

async fn function_handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    let msg = event.payload.message;

    let df = get_data_from_s3().await?;
    println!("{:?}", df);

    let response = Response {
        req_id: event.context.request_id,
        msg: say_hello(Some(&msg)),
    };

    Ok(response)
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .json()
        .with_env_filter(
            EnvFilter::builder()
                .with_default_directive(LevelFilter::INFO.into())
                .from_env_lossy(),
        )
        .with_max_level(tracing::Level::INFO)
        .with_target(false)
        .with_current_span(false)
        .without_time()
        .init();

    run(service_fn(function_handler)).await
}
