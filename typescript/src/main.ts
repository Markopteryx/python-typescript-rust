import fs from "fs";
import * as yup from "yup";
import { PlanFacet, PlanFacetSchema } from "./types";

const rawData = fs.readFileSync("allPlans.json", "utf8");
const data: PlanFacet[] = JSON.parse(rawData);

function validateData(data: PlanFacet[]) {
	for (const item of data) {
		try {
			PlanFacetSchema.validateSync(item, { strict: true });
			console.log("Plan is valid:", item.pk);
		} catch (error) {
			if (error instanceof yup.ValidationError) {
				console.log("Item that caused the error:", item);
				console.log(`Validation error for PlanFacet ${item.pk}:`, error.errors);
				break;
			} else {
				console.error("Unexpected error:", error);
				break;
			}
		}
	}
}

validateData(data);
