import cli_parser
import file_operations
import bookmark_utils
import json

def main():
    args = cli_parser.parse_arguments()

    if args.list:
        bookmarks_object_wrappers_list = list(file_operations.load_bookmarks_files(args.files))
        with open(args.output, "w") as output:
            for bookmarks_object_wrapper in bookmarks_object_wrappers_list:
                output.write(bookmarks_object_wrapper.get("name") + "\n")
                bookmark_utils.print_pretty_url_tree(bookmarks_object_wrapper.get("json").get("children"), output)
                output.write("\n")
    
    if args.merge or args.merge_to_subdir:
        if len(args.files) > 1:
            bookmarks_object_wrappers_list = list(file_operations.load_bookmarks_files(args.files))
            main_bookmarks_object = bookmarks_object_wrappers_list[0].get("json")
            if args.merge:
                for other_bookmarks_object_wrapper in bookmarks_object_wrappers_list[1:]:
                    bookmark_utils.merge_into(
                        main_bookmarks_object, 
                        other_bookmarks_object_wrapper.get("json"))
                file_operations.write_to_file(args.output, json.dumps(main_bookmarks_object, indent=4))
            elif args.merge_to_subdir:
                for other_bookmarks_object_wrapper in bookmarks_object_wrappers_list[1:]:
                    bookmark_utils.merge_to_subdir(
                        main_bookmarks_object, 
                        other_bookmarks_object_wrapper.get("json"), 
                        other_bookmarks_object_wrapper.get("name"))
                file_operations.write_to_file(args.output, json.dumps(main_bookmarks_object, indent=4))
        else:
            print("Not enough files for merge")
