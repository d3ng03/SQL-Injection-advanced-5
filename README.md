# SQL Injection Advanced Testing Tool

This repository contains a set of Python scripts designed to perform advanced SQL injection testing on WebGoat's SQL Injection Advanced challenge. The tool systematically extracts database information through blind SQL injection techniques.

## Overview

The tool consists of four main components:

1. `db.py` - Extracts database schema information
2. `table.py` - Extracts table information from each database
3. `column.py` - Extracts column information from each table
4. `value.py` - Extracts actual data values from the tables

## Features

- Blind SQL injection testing
- Database schema enumeration
- Table structure extraction
- Column information gathering
- Data value extraction
- Progress tracking with tqdm
- Binary search for efficient character extraction

## Prerequisites

- Python 3.x
- Required Python packages:
  - requests
  - tqdm

## Usage

1. Configure the target IP address and session cookie in each script
2. Run the scripts in sequence:
   ```bash
   python db.py      # Extract database information
   python table.py   # Extract table information
   python column.py  # Extract column information
   python value.py   # Extract data values
   ```

## Script Details

### db.py
- Extracts the number of databases
- Retrieves database names
- Uses binary search for efficient character extraction

### table.py
- Extracts table information from specified databases
- Enumerates all tables in each database
- Provides detailed table structure information

### column.py
- Extracts column information from specified tables
- Enumerates all columns in each table
- Provides detailed column structure information

### value.py
- Extracts actual data values from tables
- Uses binary search for efficient character extraction
- Handles multiple data types and formats

## Security Note

This tool is intended for educational purposes and should only be used on systems where you have explicit permission to perform security testing. Unauthorized use of this tool may be illegal and unethical.

## License

This project is for educational purposes only. Use responsibly and only on systems you have permission to test.