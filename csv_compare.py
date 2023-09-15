#!/usr/bin/env python
import pandas as pd
import os
import argparse
import numpy as np
from pathlib import Path
import logging

# Initialize logging
logging.basicConfig(filename='catalog_compare.log', level=logging.INFO)

def sample(location, op, header_list):
    files = list(Path(location).glob("**/*.csv"))

    if not files:
        logging.error(f"No CSV files found in the directory: {location}")
        return None

    logging.info(f"Header List: {header_list}")

    try:
        Sam = pd.concat([pd.read_csv(csvfile).assign(Sample='_'.join(os.path.basename(csvfile).split("_")[:2]))
                        for csvfile in files])

        # Strip any leading or trailing whitespace from DataFrame column names
        Sam.columns = Sam.columns.str.strip()
        SSam = Sam[["Sample"] + header_list].sort_values(by=["Sample"]).reset_index(drop=True).copy()
        SSam.to_csv(output + "/" + op + ".csv", index=False)
        return SSam

    except Exception as e:
        logging.error(f"An error occurred while processing files in {location}: {str(e)}")
        return None

def compare_excel(m1, m2, output):
    try:
        Full_comparison = m1.set_index("Sample").compare(m2.set_index("Sample"), keep_equal=True, keep_shape=True,
                                                        result_names=('Method1', 'Method2'))

        def highlight_diff(data, color='yellow'):
            attr = 'background-color: {}'.format(color)
            other = data.xs('Method1', axis='columns', level=-1)
            return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                                index=data.index, columns=data.columns)

        Full_comparison.style.apply(highlight_diff, axis=None).to_excel(output + "/Method1_vs_Method2.xlsx")
        compared = m1.set_index("Sample").compare(m2.set_index("Sample"), keep_shape=True,
                                                  result_names=('Method1', 'Method2'))
        return Full_comparison, compared

    except Exception as e:
        logging.error(f"An error occurred during comparison: {str(e)}")
        return None, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser("This code compares the dst file results between NewCatalog and OldCatalog")
    input = parser.add_argument_group(title="Input Files", description="Enter the required input files")
    input.add_argument("-m1", "--Method1", action='store', dest='csv1',
                       help="path to the directory where Catalog 1 results are stored")
    input.add_argument("-m2", "--Method2", action='store', dest='csv2',
                       help="path to the directory where Catalog 2 results are stored")
    input.add_argument("-hlist", "--header_list_file", action='store', dest='header_list_file',
                       help="path to the header list text file")
    input.add_argument("-o", "--output", action='store', dest='out', help="path to the output folder")

    args = parser.parse_args()
    P1_l = args.csv1
    P2_l = args.csv2
    output = args.out

    # Read the header list from the file
    header_list = []
    if args.header_list_file:
        try:
            with open(args.header_list_file, 'r') as f:
                header_list = f.read().strip().split(',')
        except Exception as e:
            logging.error(f"An error occurred while reading the header list file: {str(e)}")

    logging.info(f"Method 1 Directory: {P1_l}")
    logging.info(f"Method 2 Directory: {P2_l}")
    logging.info(f"Output Directory: {output}")

    m1 = sample(P1_l, "Method1", header_list)
    m2 = sample(P2_l, "Method2", header_list)

    Full_comparison, compared = compare_excel(m1, m2, output)

    if Full_comparison is not None and compared is not None:
        print("Full comparison done!")
        print("The results are stored in output/Method1_vs_Method2.xlsx")
    else:
        print("Error occurred. Check the log file catalog_compare.log for details.")
