# SQL Query Extractor - Design Document

## Overview

The SQL Query Extractor is a tool designed to extract SQL queries from code repositories, supporting both local directories and GitHub repositories. This document outlines the architecture, design decisions, and implementation details of the system.

## Architecture

The system follows a modular architecture with the following components:

### 1. Web Interface (`app/app.py`)

- Built using Streamlit for web-based interface
- Provides a user-friendly web UI for configuration and interaction
- Handles user input and displays results in real-time
- Supports both GitHub and local directory sources
- Features interactive query viewing and JSON download

### 2. CLI Interface (`app/cli.py`)

- Built using Typer for command-line interface
- Handles command-line argument parsing
- Provides user-friendly interface for configuration
- Manages the flow of execution

### 3. Flow Management (`app/flow.py`)

- Built on top of PocketFlow framework
- Orchestrates the extraction process
- Manages the sequence of operations
- Handles shared state between components
- Implements the main business logic flow

### 4. Node System (`app/nodes/`)

The system uses PocketFlow's node-based architecture where each node represents a specific operation in the extraction process. Nodes are designed to be:
- Independent and focused on a single responsibility
- Reusable across different flows
- Easy to test and maintain
- Configurable through shared state

### 5. Utility Functions (`app/utils/`)

- Contains helper functions and utilities
- Provides common functionality used across nodes
- Implements file handling, pattern matching, and other core operations

## PocketFlow Framework

The SQL Query Extractor is built using the PocketFlow framework, which provides several key benefits:

### 1. Node-Based Architecture

PocketFlow enables a modular, node-based architecture where:
- Each node represents a discrete operation in the extraction process
- Nodes can be easily composed into complex workflows
- The framework handles the flow of data between nodes
- Nodes can be reused across different flows

### 2. Flow Management

PocketFlow provides:
- Automatic orchestration of node execution
- Shared state management between nodes
- Error handling and recovery mechanisms
- Support for both sequential and parallel execution

### 3. Node Lifecycle

Each node in PocketFlow follows a clear lifecycle:
- `prep`: Prepare node-specific configuration
- `exec`: Execute the main node logic
- `post`: Process and store results in shared state

### 4. Extensibility

The framework enables:
- Easy addition of new nodes
- Custom node types for specific needs
- Flexible configuration options
- Integration with external systems

## Design Decisions

### 1. Dual Interface Approach

The system provides both web and CLI interfaces to:
- Cater to different user preferences and use cases
- Enable both interactive and scriptable usage
- Support both casual and power users
- Allow for easy integration into automated workflows

### 2. Modular Architecture

The system uses a modular design to:
- Enable easy addition of new features
- Facilitate testing of individual components
- Allow for future extensibility
- Maintain separation of concerns

### 3. Node-Based Processing

The node-based approach was chosen because it:
- Provides clear separation of processing steps
- Makes the system more maintainable
- Allows for easy modification of the processing pipeline
- Enables parallel processing if needed in the future

### 4. Configuration Management

Configuration is handled through:
- Command-line arguments for user input
- Web interface for interactive configuration
- Shared state dictionary for internal configuration
- Default values for common use cases
- Environment variables for sensitive data

### 5. File Processing

File processing includes:
- Pattern-based file filtering
- Size limits to prevent memory issues
- Support for multiple file types
- Exclusion patterns for common directories

## Implementation Details

### 1. Web Interface

The Streamlit interface provides:
- Source selection (GitHub or local)
- Visual configuration of file patterns
- Real-time extraction status
- Interactive query viewing
- JSON download capability
- Error handling and user feedback

### 2. File Processing

- Files are processed based on include/exclude patterns
- Maximum file size limit prevents memory issues
- Support for both local and remote (GitHub) repositories
- Efficient file traversal and filtering

### 3. Query Extraction

- SQL queries are identified using pattern matching
- Support for multiple SQL dialects
- Context preservation for extracted queries
- Output in JSON format for easy processing

### 4. GitHub Integration

- Support for both public and private repositories
- Personal access token for authentication
- Rate limit handling
- Efficient repository cloning and processing

## Future Considerations

- Add support for more SQL dialects
- Implement parallel processing for large repositories
- Add query analysis and visualization features
- Support for more source control systems
- Enhanced web interface features

## Security Considerations

1. **Authentication**
   - Secure handling of GitHub tokens
   - Environment variable support for sensitive data
   - No storage of credentials

2. **File Processing**
   - Size limits to prevent memory issues
   - Safe file handling practices
   - Input validation and sanitization