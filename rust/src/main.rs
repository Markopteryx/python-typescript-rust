// Fix the error below with least amount of modification to the code
fn main() {
    let x: i32 = 5; // Uninitialized but used, ERROR !

    assert_eq!(x, 5);
    println!("Success!");
}
