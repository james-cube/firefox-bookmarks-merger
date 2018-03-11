def get_bookmarks_from(bookmarks_object, source):
    bookmarks_groups = bookmarks_object.get("children")
    for bookmarks_group in bookmarks_groups:
        if bookmarks_group.get("root") == source:
            return bookmarks_group.get("children")
    return []
    
def get_bookmarks_from_toolbar(bookmarks_object):
    return get_bookmarks_from(bookmarks_object, "toolbarFolder")

def get_bookmarks_from_menu(bookmarks_object):
    return get_bookmarks_from(bookmarks_object, "bookmarksMenuFolder")

def get_bookmarks_from_other(bookmarks_object):
    return get_bookmarks_from(bookmarks_object, "unfiledBookmarksFolder")

def flatten_bookmarks(bookmarks):
    result = []
    if bookmarks != None:
        for bookmark in bookmarks:
            if bookmark.get("type") == "text/x-moz-place-container":
                children_bookmarks = flatten_bookmarks(bookmark.get("children"))
                for child in children_bookmarks:
                    result.append(child)
            else:
                result.append(bookmark)
    return result

def strip_ids(bookmarks):
    if bookmarks != None:
        for bookmark in bookmarks:
            if bookmark.get("type") == "text/x-moz-place-container":
                strip_ids(bookmark.get("children"))
            bookmark.pop("id", None)
            bookmark.pop("guid", None)
            bookmark.pop("index", None)

def remove_from_tree(bookmarks, removal):
    if bookmarks != None:
        removal_index = -1
        for i in range(len(bookmarks)):
            bookmark = bookmarks[i]
            if bookmark.get("type") == "text/x-moz-place-container":
                remove_from_tree(bookmark.get("children"), removal)
            elif bookmark.get("type") == "text/x-moz-place" and bookmark.get("uri") == removal.get("uri"):
                removal_index = i
        if removal_index >= 0:
            bookmarks.pop(removal_index)

def merge_into_bookmarks(main_bookmarks, bookmarks):
    flattened_bookmarks = flatten_bookmarks(bookmarks)
    for bookmark in flattened_bookmarks:
        if has_duplicate(main_bookmarks, bookmark):
            remove_from_tree(bookmarks, bookmark)
    strip_ids(bookmarks)
    for bookmark in bookmarks:
        main_bookmarks.append(bookmark)

def merge_into(main_bookmarks_object, other_bookmarks_object):
    merge_into_bookmarks(
        get_bookmarks_from_toolbar(main_bookmarks_object), 
        get_bookmarks_from_toolbar(other_bookmarks_object))
    merge_into_bookmarks(
        get_bookmarks_from_menu(main_bookmarks_object), 
        get_bookmarks_from_menu(other_bookmarks_object))
    merge_into_bookmarks(
        get_bookmarks_from_other(main_bookmarks_object), 
        get_bookmarks_from_other(other_bookmarks_object))

def merge_bookmarks_to_subdir(main_bookmarks, bookmarks, subdir_name):
    strip_ids(bookmarks)
    subdir = {"type": "text/x-moz-place-container", "title": subdir_name, "children": bookmarks}
    main_bookmarks.append(subdir)

def merge_to_subdir(main_bookmarks_object, other_bookmarks_object, subdir_name):
    merge_bookmarks_to_subdir(
        get_bookmarks_from_toolbar(main_bookmarks_object), 
        get_bookmarks_from_toolbar(other_bookmarks_object), 
        subdir_name)
    merge_bookmarks_to_subdir(
        get_bookmarks_from_menu(main_bookmarks_object), 
        get_bookmarks_from_menu(other_bookmarks_object),
        subdir_name)
    merge_bookmarks_to_subdir(
        get_bookmarks_from_other(main_bookmarks_object), 
        get_bookmarks_from_other(other_bookmarks_object), 
        subdir_name)

def print_pretty_url_tree(bookmarks, output, padding = 1):
    if bookmarks != None:
        for bookmark in bookmarks:
            if bookmark.get("type") == "text/x-moz-place-container":
                output.write((padding * "\t") + bookmark.get("title") + "\n")
                print_pretty_url_tree(bookmark.get("children"), output, padding + 1)
            elif bookmark.get("type") == "text/x-moz-place":
                output.write((padding * "\t") + bookmark.get("title") + " - " + bookmark.get("uri") + "\n")
            else:
                output.write((padding * "\t") + "----\n")

def has_duplicate(bookmarks, bookmark):
    flattened_bookmarks = flatten_bookmarks(bookmarks)
    duplicates = [b for b in flattened_bookmarks if b.get("uri") == bookmark.get("uri")]
    return len(duplicates) > 0
 
