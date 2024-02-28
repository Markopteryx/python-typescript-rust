use futures::stream::{self, StreamExt};
use jwalk::WalkDir;
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use std::time::Instant;
use tokio::runtime::Runtime;
use zip::ZipArchive;

async fn hash_file(path: PathBuf) -> io::Result<(String, PathBuf)> {
    let mut file = File::open(&path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024];

    loop {
        let n = file.read(&mut buffer)?;
        if n == 0 {
            break;
        }
        hasher.update(&buffer[..n]);
    }

    let hash = format!("{:x}", hasher.finalize());
    Ok((hash, path))
}

async fn unzip_file(file_path: &Path, destination: &Path) -> io::Result<()> {
    let file = File::open(file_path)?;
    let mut archive = ZipArchive::new(file)?;

    for i in 0..archive.len() {
        let mut file = archive.by_index(i)?;
        let outpath = destination.join(file.mangled_name());

        if file.name().ends_with('/') {
            fs::create_dir_all(&outpath)?;
        } else {
            if let Some(p) = outpath.parent() {
                if !p.exists() {
                    fs::create_dir_all(p)?;
                }
            }
            let mut outfile = File::create(&outpath)?;
            io::copy(&mut file, &mut outfile)?;
        }
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let start_dir = "docu";
    let start = Instant::now();

    let rt = Runtime::new()?;

    rt.block_on(async {
        let mut paths: Vec<PathBuf> = Vec::new();
        let mut zip_paths: Vec<PathBuf> = Vec::new();

        for entry in WalkDir::new(start_dir)
            .sort(true)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let path = entry.path().to_path_buf();
            if entry.file_type().is_file() {
                if let Some(extension) = path.extension() {
                    if extension == "zip" {
                        zip_paths.push(path.clone());
                        continue;
                    }
                }
                paths.push(path);
            }
        }

        stream::iter(zip_paths)
            .map(|zip_path| {
                let start_dir = PathBuf::from(start_dir);
                tokio::spawn(async move { unzip_file(&zip_path, &start_dir.join("unzip")).await })
            })
            .buffer_unordered(100)
            .collect::<Vec<_>>()
            .await;

        let mut hash_map: HashMap<String, Vec<PathBuf>> = HashMap::new();

        let hashes = stream::iter(paths)
            .map(|path| tokio::spawn(hash_file(path)))
            .buffer_unordered(100)
            .collect::<Vec<_>>()
            .await;

        for hash_result in hashes.into_iter().flatten().flatten() {
            let (hash, path) = hash_result;
            hash_map.entry(hash).or_default().push(path);
        }

        println!("Time taken: {:.2}s", start.elapsed().as_secs_f64());
        println!("Total unique files by hash: {}", hash_map.len());
    });

    Ok(())
}
