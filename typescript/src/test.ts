/**
 *
 * __Welcome to our coding challenge!__
 * we understand that a test environment is superficial and stressful
 * don't worry if you do something silly
 *
 * __We have 7 questions__
 * answer each question and demonstrate correct results to the interviewer
 * you will see comments with expected results
 *
 * __There is time pressure__
 * certain questions take up less time then others
 * if you get stuck on a question just move on to the next question and come back later
 * don't worry about edge cases, just follow the happy path
 * if you have time at the end you can discuss edge cases and complexity
 * */

/**
 * question 1
 * write a function that when given a list of records
 * returns the currency of the last record in that array
 * */
type CurrencyRecord = { currency: string; quantity: number };

const records: CurrencyRecord[] = [
	{ currency: "BTC", quantity: 1 },
	{ currency: "ETH", quantity: 9 },
	{ currency: "ICP", quantity: 11000 },
]; // => "ICP"

const getLastCurrency = (records: CurrencyRecord[]): string => {
	return records[records.length - 1].currency;
};

console.log(getLastCurrency(records)); // "ICP"

/**
 * question 2
 * write a function that given a list of integer numbers
 * returns the total value of multiplying all those numbers together
 * */
const input: number[] = [1, 2, 3, 2]; // => 12

const multiplyAll = (numbers: number[]): number => {
	return numbers.reduce((acc, num) => acc * num, 1);
};

console.log(multiplyAll(input)); // 12

/**
 * question 3
 * write a named function called suffix
 * that when given a string
 * returns a function that adds this string as a suffix e.g.
 * suffix("ing")("feel") => "feeling"
 * */
const suffixStr = "ing";
const prefixStr = "feel";

function suffix(suffixStr: string) {
	return (word: string): string => word + suffixStr;
}

console.log(suffix(suffixStr)(prefixStr)); // "feeling"

/**
 * question 4
 * write a function that takes an array and returns the total of all numbers in that array
 * and any children arrays
 * */
type NestedArray = (number | NestedArray)[];

const exampleOne: NestedArray = [1, 2, 3]; // => 6
const exampleTwo: NestedArray = [[1], 2, [3, 5, [4, [5]]]]; // => 20

const sumNestedArray = (array: NestedArray): number => {
	return array.reduce<number>((acc, item) => {
		if (Array.isArray(item)) {
			return acc + sumNestedArray(item);
		} else {
			return acc + item;
		}
	}, 0);
};

console.log(sumNestedArray(exampleOne)); // 6
console.log(sumNestedArray(exampleTwo)); // 20

/**
 * question 5
 * write a function that given a list
 * return the first string that is out of order
 * */
const unorderedList: string[] = [
	"apple",
	"banana",
	"cat",
	"elephant",
	"dog",
	"fish",
]; // => "dog"

const findFirstOutOfOrder = (list: string[]): string | null => {
	for (let i = 1; i < list.length; i++) {
		if (list[i] < list[i - 1]) {
			return list[i];
		}
	}
	return null;
};

console.log(findFirstOutOfOrder(unorderedList)); // "dog"

/**
 * question 6
 * write a function that given a string with random characters
 * find the character that is repeated the second most number of times
 * return this character along with the total count of this character
 * */
const ranStr: string = "aaaccbanantttdf"; // => ["t", 3]

const findSecondMostRepeated = (str: string): [string, number] | null => {
	const charCount: { [key: string]: number } = {};

	for (const char of str) {
		charCount[char] = (charCount[char] || 0) + 1;
	}

	const sortedChars = Object.entries(charCount).sort((a, b) => b[1] - a[1]);

	if (sortedChars.length < 2) {
		return null;
	}

	return [sortedChars[1][0], sortedChars[1][1]];
};

console.log(findSecondMostRepeated(ranStr)); // ["t", 3]

/**
 * question 7
 * we have an array generated from parsing a CSV
 * create a function that formats this array to
 * {price: number, currency: string}[]
 * */
const sampleData: string[] = [
	"$10, 000; ETH ;",
	"$100; BTC\n",
	"$11000; BTC;",
	"$2,000,000;NEX;",
	"2400;USDT ",
	"200;USDT",
]; // => e.g. first element is {price: 10000, currency: "ETH"}

type FormattedData = { price: number; currency: string };

const formatCSVData = (data: string[]): FormattedData[] => {
	return data.map((item) => {
		const [pricePart, currencyPart] = item
			.split(";")
			.map((part) => part.trim());
		const price = parseFloat(pricePart.replace(/[^0-9.-]+/g, ""));
		const currency = currencyPart.replace(/[^A-Z]+/g, "");
		return { price, currency };
	});
};

console.log(formatCSVData(sampleData));
// [
//     { price: 10000, currency: "ETH" },
//     { price: 100, currency: "BTC" },
//     { price: 11000, currency: "BTC" },
//     { price: 2000000, currency: "NEX" },
//     { price: 2400, currency: "USDT" },
//     { price: 200, currency: "USDT" }
// ]
