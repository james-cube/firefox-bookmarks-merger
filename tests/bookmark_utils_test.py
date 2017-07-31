import unittest
import io
from firefox_bookmarks_merger import file_operations
from firefox_bookmarks_merger import bookmark_utils

def load_testcase(filename):
    bookmarks_object_wrapper = file_operations.load_bookmarks_file(filename)
    return bookmarks_object_wrapper.get("json")

class FirefoxBookmarksMergerTestSuite(unittest.TestCase):
    
    def test_flatten_bookmarks(self):
        bookmarks_object = load_testcase("tests/recursion_testcase.json")
        menu_bookmarks = bookmark_utils.get_bookmarks_from_menu(bookmarks_object)
        flattened_menu_bookmarks = bookmark_utils.flatten_bookmarks(menu_bookmarks)
        self.assertEqual(len(flattened_menu_bookmarks), 4)
    
    def test_strip_ids(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        
        menu_bookmarks = bookmark_utils.get_bookmarks_from_menu(bookmarks_object)
        bookmark_utils.strip_ids(menu_bookmarks)
        
        flattened_menu_bookmarks = bookmark_utils.flatten_bookmarks(menu_bookmarks)
        for bookmark in flattened_menu_bookmarks:
            self.assertEqual(bookmark.get("id"), None)
            self.assertEqual(bookmark.get("guid"), None)
            self.assertEqual(bookmark.get("index"), None)
    
    def test_get_bookmarks_from_toolbar(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        toolbar_bookmarks = bookmark_utils.get_bookmarks_from_toolbar(bookmarks_object)
        self.assertEqual(len(toolbar_bookmarks), 1)
    
    def test_get_bookmarks_from_menu(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        menu_bookmarks = bookmark_utils.get_bookmarks_from_menu(bookmarks_object)
        self.assertEqual(len(menu_bookmarks), 3)

    def test_get_bookmarks_from_other(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        menu_bookmarks = bookmark_utils.get_bookmarks_from_other(bookmarks_object)
        self.assertEqual(len(menu_bookmarks), 0)
 
    def test_get_bookmarks_from_invalid_source(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        empty_bookmarks = bookmark_utils.get_bookmarks_from(bookmarks_object, "bullshit")
        self.assertEqual(len(empty_bookmarks), 0)
    
    def test_has_duplicate_in_menu(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        
        menu_bookmarks = bookmark_utils.get_bookmarks_from_menu(bookmarks_object)
        flattened_menu_bookmarks = bookmark_utils.flatten_bookmarks(menu_bookmarks)
        #testing against self should return all true
        for bookmark in flattened_menu_bookmarks:
            self.assertTrue(bookmark_utils.has_duplicate(menu_bookmarks, bookmark))
        #testing against unexpected bookmark 
        self.assertFalse(bookmark_utils.has_duplicate(menu_bookmarks, { "uri" : "unexpected" }))
 
    def test_remove_from_tree(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        menu_bookmarks = bookmark_utils.get_bookmarks_from_menu(bookmarks_object)
        flattened_menu_bookmarks = bookmark_utils.flatten_bookmarks(menu_bookmarks)
        for bookmark in flattened_menu_bookmarks:
            bookmark_utils.remove_from_tree(menu_bookmarks, bookmark)
        flattened_again = bookmark_utils.flatten_bookmarks(menu_bookmarks)
        self.assertEqual(len(flattened_again), 1)#one separator "bookmark" left
        
    def test_merge_to_subdir(self):
        bookmarks_object_1 = load_testcase("tests/testcase1.json")
        bookmarks_object_2 = load_testcase("tests/testcase2.json")
        bookmark_utils.merge_to_subdir(bookmarks_object_1, bookmarks_object_2, "tests/testcase2.json")
        other_bookmarks = bookmark_utils.get_bookmarks_from_other(bookmarks_object_1)
        self.assertEqual(len(other_bookmarks), 1)
        self.assertEqual(other_bookmarks[0].get("title"), "tests/testcase2.json")
        self.assertEqual(other_bookmarks[0].get("type"), "text/x-moz-place-container")
        self.assertEqual(len(other_bookmarks[0].get("children")), 1)

    def test_merge_into(self):
        bookmarks_object_1 = load_testcase("tests/testcase1.json")
        bookmarks_object_2 = load_testcase("tests/testcase2.json")
        bookmark_utils.merge_into(bookmarks_object_1, bookmarks_object_2)
        menu_bookmarks = bookmark_utils.get_bookmarks_from_menu(bookmarks_object_1)
        toolbar_bookmarks = bookmark_utils.get_bookmarks_from_toolbar(bookmarks_object_1)
        other_bookmarks = bookmark_utils.get_bookmarks_from_other(bookmarks_object_1)
        self.assertEqual(len(menu_bookmarks), 5)
        self.assertEqual(len(toolbar_bookmarks), 3)
        self.assertEqual(len(other_bookmarks), 1)
    
    def test_print_pretty_url_tree(self):
        bookmarks_object = load_testcase("tests/testcase1.json")
        
        output = io.StringIO()
        bookmark_utils.print_pretty_url_tree(bookmarks_object.get("children"), output)
        pretty_print = output.getvalue()
        with open("tests/pretty_print_expected.txt") as expected:
            self.assertEqual(pretty_print, expected.read())
    

if __name__ == '__main__':
    unittest.main() 
