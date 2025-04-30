from pocketflow import Node

import json
import os

class GenerateOutput(Node):
    def prep(self, shared):
        # Get output path and data from shared
        output_path = shared.get("output_path", "artifacts/queries.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        return {
            "output_path": output_path,
            "data": shared.get("processed_queries", {})
        }
    
    def exec(self, prep_data):
        # Write data to JSON file
        with open(prep_data["output_path"], "w") as f:
            json.dump(prep_data["data"], f, indent=4)
        return prep_data["output_path"]
    
    def post(self, shared, prep_res, exec_res):
        # Store output path in shared
        shared["output_path"] = exec_res
