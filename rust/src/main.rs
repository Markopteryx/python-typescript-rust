fn main() {
    let num = "ten";
    let result: i32 = num.parse().unwrap(); // Error: trying to parse a string to i32

    let mut vector = vec![1, 2, 3];
    println!("Fourth element: {}", vector[3]); // Error: out-of-bounds access

    let unused_variable = 42; // Warning: unused variable
}
