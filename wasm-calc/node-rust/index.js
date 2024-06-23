"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const rust_calc_1 = require("rust-calc");
console.time("fibonacci");
// function multiplyMatrices(A: number[][], B: number[][]): number[][] {
// 	const n = A.length;
// 	const result: number[][] = Array.from({ length: n }, () => Array(n).fill(0));
// 	for (let i = 0; i < n; i++) {
// 		for (let j = 0; j < n; j++) {
// 			for (let k = 0; k < n; k++) {
// 				result[i][j] += A[i][k] * B[k][j];
// 			}
// 		}
// 	}
// 	return result;
// }
const n = 1000; // Adjust this value to increase or decrease the computational load
const a = new Float64Array(n * n).map(() => Math.random());
const b = new Float64Array(n * n).map(() => Math.random());
// multiplyMatrices(A, B);
(0, rust_calc_1.multiply_matrices)(a, b, n);
console.timeEnd("fibonacci");
