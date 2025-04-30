from pocketflow import BatchNode
from app.utils.call_llm import call_llm
import json
import re


class ProcessQueries(BatchNode):
    
    def prep(self, shared):
        # Get queries from shared
        queries = shared.get("queries", [])
        self.llm_provider = shared.get("llm_provider", "ollama")
        return queries  # Return list of queries directly

    def exec(self, query):  # query is passed directly
        print(f"Processing code: {query['raw_query']}")

        instruction = "You are a helpful assistant expert in extracting SQL queries in structured JSON format from code accurately."

        prompt = f"""
            Task:
            Analyze the following code and extract the Postgres SQL query along with metadata in JSON format:
            {query['raw_query']}

            Instructions:
            - Provide a JSON object with:
                1. "name" — an appropriate name for the query
                2. "description" — a concise description of what the query does
                3. "query" — the extracted Postgres SQL query
            - Return ONLY the JSON object. No additional explanations.
            - Ensure the output is:
                - Valid, directly parseable JSON
                - Free from escape sequences like \\_ or \\*
                - If the SQL string is split across multiple lines using escaped characters like \n, concatenate and clean it to form a valid SQL query. Remove all escape characters (\n, \", etc.), and reconstruct the query as a readable, properly formatted SQL string.
                - Not wrapped inside markdown or code blocks

            Example:
            {{
            "name": "Insert student",
            "description": "Inserts a new student record into the database",
            "query": "INSERT INTO students (name, age, gender) VALUES ($1, $2, $3)"
            }}

            Avoid:
            - Adding introductory text or commentary
            - Incorrect JSON formats
            """

        try:
            # Call LLM with the selected provider
            llm_response = call_llm(
                instruction=instruction,
                prompt=prompt,
                provider_name=self.llm_provider
            )
            print(llm_response)
            
            query = self._parse_json(llm_response)

            return query
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return None

    def post(self, shared, prep_res, exec_res):
        # Store processed queries in shared
        shared["processed_queries"] = exec_res


    def _parse_json(self, result: str):
        # Ensure valid JSON
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in LLM response")

        json_data = json_match.group(0)
        response_dict = json.loads(json_data)
        return response_dict
