import { PassThrough } from "stream";
import { S3Client } from "@aws-sdk/client-s3";
import { Upload } from "@aws-sdk/lib-storage";
//@ts-ignore
import { ParquetSchema, ParquetWriter } from "parquetjs-lite";

const client = new S3Client({ region: "ap-southeast-2" });

const schema = new ParquetSchema({
	id: { type: "INT64" },
	name: { type: "UTF8" },
	age: { type: "INT32" },
	balance: { type: "FLOAT" },
});

async function uploadParquetToS3() {
	const passThrough = new PassThrough();

	const writer = await ParquetWriter.openStream(schema, passThrough);

	const data = [];

	for (let i = 0; i < 1000; i++) {
		data.push({ id: i, name: `Name ${i}`, age: i, balance: i * 100 });
	}

	for (const row of data) {
		await writer.appendRow(row);
	}

	await writer.close();

	const uploader = new Upload({
		client: client,
		params: {
			Bucket: "rust-s3",
			Key: "your-object-key.parquet",
			Body: passThrough,
		},
	});

	try {
		const result = await uploader.done();
		console.log("Successfully uploaded:", result);
	} catch (err) {
		console.error("Error uploading:", err);
	}
}

uploadParquetToS3().catch((err) => {
	console.error("Error:", err);
});
