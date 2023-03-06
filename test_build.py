from src.build import build
import unittest
import os

class TestBuild(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        build("./test/certificados_test.pdf", "./test/output")

    def testCreateFolder(self):
        # Check if the folder to store pages was created
        self.assertTrue(os.path.isdir("./test/output"))

    def testPageInFolder(self):
        # Check if the page in folder has correct name (nit)
        self.assertTrue(os.path.isfile("./test/output/123456789.pdf"))


if __name__ == '__main__':
    unittest.main()