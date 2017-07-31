[![Build Status](https://travis-ci.org/james-cube/firefox-bookmarks-merger.svg?branch=master)](https://travis-ci.org/james-cube/firefox-bookmarks-merger)

# firefox-bookmarks-merger

Tool for merging firefox bookmarks backups. Designed for people who don't want to use cloud based tools like firefox sync, plugins, want to version control their bookmarks backups or have any other reason to do this locally.

## Usage

### How to backup/restore firefox bookmarks? (up to date with Firefox 54)

In top menu `Bookmarks` under `Show All Bookmarks` there is button `Import and Backup` which allows you to perform those operations either using `json` or `html` file. This module uses and generates `json` backups. 

### How to use the tool?

#### Listing bookmarks

Creating simple tree structure showing all firefox bookmarks in menu, toolbar and starred.

`python firefox_bookmarks_merger --list --files bookmarks-20XX-XX-XX.json --output output.txt`

[Example output](https://github.com/james-cube/firefox-bookmarks-merger/blob/master/tests/pretty_print_expected.txt)

#### Merge

Merge two or more backup files into one. First one is considered "primary". Bookmarks from next backup files will be appended (if there is no duplication). Folders with same name are not merged, but duplication removal is recursive.

`python firefox_bookmarks_merger --merge --files bookmarks-20XX-XX-XX.json bookmarks-20YY-YY-YY.json --output output.json`

#### Merge to subdirectory

Simple merge of two or more backup files. Each additional backup after primary is given his own folder in primary backup and all bookmarks are stored there, without duplicate removal. To put it simple, in example below, there will be folder named `bookmarks-20YY-YY-YY.json` generated alongside bookmarks from `bookmarks-20XX-XX-XX.json` with whole list stored there. 

`python firefox_bookmarks_merger --merge-to-subdir --files bookmarks-20XX-XX-XX.json bookmarks-20YY-YY-YY.json --output output.json`

### All program arguments

```
usage: firefox_bookmarks_merger [-h] (--list | --merge | --merge-to-subdir)
                                --files FILES [FILES ...] --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --list                Print titles and urls of all bookmarks
  --merge               Merge bookmarks with duplicate removal
  --merge-to-subdir     Create additional folder for merged bookmarks
  --files FILES [FILES ...]
                        List of files to process
  --output OUTPUT       Output file
```

### Other modules 

I also developed similar tool for session management [Firefox Session Merger](https://github.com/james-cube/firefox-session-merger)
