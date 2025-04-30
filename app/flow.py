from pocketflow import Flow
from app.nodes.fetch_repository import FetchRepository
from app.nodes.extract_queries import ExtractQueries
from app.nodes.process_queries import ProcessQueries
from app.nodes.generate_output import GenerateOutput

def create_extract_flow() -> Flow:
    """
    Create and return the SQL query extraction flow.
    
    Returns:
        Flow object ready to run
    """
    # Create nodes
    fetch = FetchRepository()
    extract = ExtractQueries()
    process = ProcessQueries()
    generate = GenerateOutput()
    
    # Connect nodes
    fetch >> extract >> process >> generate
    
    # Create and return flow
    return Flow(start=fetch) 