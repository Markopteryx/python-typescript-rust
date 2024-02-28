use jwalk::WalkDir;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let start_dir = "docu"; // Adjust this path as needed

    // Initialize a vector to hold the paths
    let mut paths = Vec::new();

    // Recursively iterate over the directory, sorting by name
    for entry in WalkDir::new(start_dir).sort(true) {
        let entry = entry?; // Handle the Result, propagating errors
                            // Append the path to the vector
        paths.push(entry.path().display().to_string());
    }

    // Print the total number of paths collected
    println!("Total paths: {}", paths.len());

    Ok(())
}
