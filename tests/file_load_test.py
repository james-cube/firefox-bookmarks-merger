import unittest
from firefox_bookmarks_merger import file_operations

class FileLoadTestSuite(unittest.TestCase):

    def test_file_load(self):
        bookmarks_object_wrapper = file_operations.load_bookmarks_file("tests/testcase1.json")
        self.assertEqual(bookmarks_object_wrapper.get("name"), "tests/testcase1.json")
        bookmarks_object = bookmarks_object_wrapper.get("json")
        self.assertEqual(bookmarks_object.get("root"), "placesRoot")
        self.assertEqual(len(bookmarks_object.get("children")), 3)

    def test_multiple_file_load(self):
        bookmarks_object_list = list(file_operations.load_bookmarks_files(["tests/testcase1.json", "tests/testcase2.json"]))
        self.assertEqual(len(bookmarks_object_list), 2) 


if __name__ == '__main__':
    unittest.main() 
