# CSV / Catalog Comparison Tool

## Overview

The Catalog Comparison Tool is a Python script that compares catalog results between two methods, Method 1 and Method 2. This tool is designed for bioinformatics and data analysis tasks.

## Usage

To use the script, run the following command:

```bash
python Catalog_compare.py -m1 /path/to/Method1/csv/dir -m2 /path/to/Method2/csv/dir -hlist /path/to/header/list.txt -o /path/to/output/dir
```

### Command Line Arguments

- `-m1` or `--Method1`: Path to Method1's CSV directory.
- `-m2` or `--Method2`: Path to Method2's CSV directory.
- `-hlist` or `--header_list_file`: Path to the header list text file (comma-separated).
- `-o` or `--output`: Path to the output directory.

## Input

- The tool expects CSV files in Method1 and Method2 directories with the same structure and column names. 
- Specify columns to compare using the header list file.

## Output

The script generates two outputs:

1. **Comparison Results**: CSV files with selected columns and sample names in the output directory.
2. **Comparison Report**: An Excel file named `Method1_vs_Method2.xlsx` highlighting differences.

## Logging

Log messages are saved in `catalog_compare.log` for troubleshooting.

#### Have a GOOD DAY 🌻
