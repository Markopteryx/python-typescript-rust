import fs from "fs";
import path from "path";
import { promisify } from "util";

interface User {
	name: string;
	age: number;
}

function getUser(user: User) {
	console.log("User details: ", user);
}

const newUser: User = {
	name: "John Doe",
	age: 30,
};

getUser(newUser);

class Product {
	constructor(
		public id: number,
		public name: string,
		public price: number,
	) {}
	displayProduct() {
		console.log(
			`Product ID: ${this.id} Name: ${this.name} Price: $${this.price}`,
		);
	}
}

const product = new Product(1, "Laptop", 1500);
product.displayProduct();
