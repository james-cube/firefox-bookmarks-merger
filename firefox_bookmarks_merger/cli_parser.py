import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='Print titles and urls of all bookmarks')
    group.add_argument('--merge', action='store_true', help='Merge bookmarks with duplicate removal')
    group.add_argument('--merge-to-subdir', action='store_true', help='Create additional folder for merged bookmarks')
    parser.add_argument('--files', dest='files', help='List of files to process', nargs='+', required=True)
    parser.add_argument('--output', dest='output', help='Output file', required=True)
    return parser.parse_args()
