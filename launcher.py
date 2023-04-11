import subprocess
from argparse import ArgumentParser
import sys

# date = "2023-04-01"
parser = ArgumentParser()
parser.add_argument("-d", "--date", dest="date", type=str, help="date")
args = parser.parse_args()
    
if args.date:
    date = args.date
else:
    sys.exit("Please give a date")

# # python ./download/download.py -d 2023-04-02
# subprocess.run(["python", "download/download.py",
#                 "-d", "{}".format(date)])

# # python ./utilities/file_merger.py -d 2023-04-02
# subprocess.run(["python", "utilities/file_merger.py",
#                 "-d", "{}".format(date)])

# python ./analysis/analyze_transactions_graph.py -c "config.json" -d 2023-04-02
subprocess.run(["python", "analysis/analyze_transactions_graph.py",
                "-c", "config.json",
                "-d", "{}".format(date)])

# python ./analysis/analyze_random_graph.py -c "config_random.json" -d 2023-04-02
subprocess.run(["python", "analysis/analyze_random_graph.py",
                "-c", "config_random.json",
                "-d", "{}".format(date)])

# python ./analysis/printer.py -d 2023-04-02
subprocess.run(["python", "analysis/printer.py",
                "-d", "{}".format(date)])
