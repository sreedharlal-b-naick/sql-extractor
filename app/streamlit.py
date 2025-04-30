import streamlit as st
import os
from app.flow import create_extract_flow
import json
from pathlib import Path

def main():
    st.set_page_config(
        page_title="SQL Query Extractor",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("SQL Query Extractor")
    st.markdown("Extract SQL queries from GitHub repositories or local directories")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # LLM Configuration
        st.subheader("LLM Configuration")
        provider_name = st.selectbox(
            "Select LLM Provider",
            ["ollama", "groq", "gemini"],
            index=0
        )
        
        if provider_name != "ollama":
            api_key = st.text_input(f"{provider_name.upper()} API Key", type="password")
            if api_key:
                os.environ[f"{provider_name.upper()}_API_KEY"] = api_key
        
        # Source selection
        st.subheader("Source Configuration")
        source_type = st.radio(
            "Select source type:",
            ["GitHub Repository", "Local Directory"]
        )
        
        if source_type == "GitHub Repository":
            repo_url = st.text_input("GitHub Repository URL")
            github_token = st.text_input("GitHub Token (optional)", type="password")
        else:
            local_dir = st.text_input("Local Directory Path", value="tests/data")
        
        # File patterns
        st.subheader("File Patterns")
        include_patterns = st.multiselect(
            "Include patterns",
            ["*.sql", "*.erl", "*.py", "*.java", "*.js", "*.ts"],
            default=["*.sql", "*.erl"]
        )
        
        exclude_patterns = st.multiselect(
            "Exclude patterns",
            ["venv/*", ".venv/*", "*test*", "tests/*", "docs/*", "examples/*", "v1/*",
             "dist/*", "build/*", "experimental/*", "deprecated/*", "legacy/*", ".git/*",
             ".github/*", ".next/*", ".vscode/*", "obj/*", "bin/*", "node_modules/*", "*.log"],
            default=["venv/*", ".venv/*", "*test*", "tests/*", "docs/*", "examples/*"]
        )
        
        # File size limit
        max_file_size = st.number_input(
            "Maximum file size (bytes)",
            min_value=1000,
            value=1000000,
            step=1000
        )
    
    # Main content area
    if st.button("Extract Queries"):
        with st.spinner("Extracting queries..."):
            # Prepare shared configuration
            shared = {
                "include_patterns": include_patterns,
                "exclude_patterns": exclude_patterns,
                "max_file_size": max_file_size,
                "llm_provider": provider_name
            }
            
            if source_type == "GitHub Repository":
                if not repo_url:
                    st.error("Please enter a GitHub repository URL")
                    st.stop()
                shared.update({
                    "repo_url": repo_url,
                    "github_token": github_token,
                    "local_dir": "artifacts/repo",
                    "output_path": "artifacts/queries.json"
                })
            else:
                if not os.path.exists(local_dir):
                    st.error(f"Directory not found: {local_dir}")
                    st.stop()
                shared.update({
                    "local_dir": local_dir,
                    "output_path": "artifacts/queries.json"
                })
            
            # Create and run the flow
            extract_flow = create_extract_flow()
            extract_flow.run(shared)
            
            # Display results
            st.success("Query extraction completed!")
            
            # Read and display the results
            output_path = shared["output_path"]
            if os.path.exists(output_path):
                with open(output_path, 'r') as f:
                    queries = json.load(f)
                
                st.subheader("Extracted Queries")
                st.write(f"Found {len(queries)} queries")
                
                # Create a download button for the JSON file
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="Download Queries (JSON)",
                        data=f,
                        file_name="queries.json",
                        mime="application/json"
                    )
                
                # Display queries in an expandable section
                with st.expander("View Queries"):
                    for query in queries:
                        st.code(query, language="sql")
            else:
                st.error("No queries were found or extracted")

if __name__ == "__main__":
    main() 