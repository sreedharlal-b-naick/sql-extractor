from pocketflow import BatchNode
import re

class ExtractQueries(BatchNode):
    def prep(self, shared):
        # Get files from shared state (output from FetchRepository)
        files = shared.get("files", [])  # List of (path, content) tuples
        return files  # Return list of files directly
    
    def exec(self, file_data):  # file_data is a tuple of (path, content)
        file_path, content = file_data
        print(f"Processing file: {file_path}")
        
        queries = []
        
        # SQL query pattern - matches text between SQL keywords
        query_pattern = r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP).*?(?=;|$)'
        
        try:
            # Find all queries in the file content
            matches = re.finditer(query_pattern, content, re.DOTALL)
            for match in matches:
                query = match.group().strip()
                if query:
                    queries.append({
                        "file": file_path,
                        "raw_query": query
                    })
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return []
            
        return queries
    
    def post(self, shared, prep_res, exec_res):
        # Flatten the list of lists into a single list of queries
        flattened_queries = [query for file_queries in exec_res for query in file_queries]
        # Store extracted queries in shared
        shared["queries"] = flattened_queries 

