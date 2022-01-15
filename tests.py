import os
from challenge import FileGetter

class TestFileGetter:
      url = 'https://oto-public.s3.amazonaws.com/natal2021.zip'
      path = './data/natal2021.zip'
      file_getter = FileGetter(url, path)
    
      def test_download_file(self):
          self.file_getter._download_file()
          content = self.file_getter.file_content
          assert isinstance(content, bytes) 

      def test_save_to_file(self): 
          assert self.file_getter._save_to_file() == self.path 
      
      def test_unzip_file(self):
          assert self.file_getter._unzip_file() == None
          assert self.file_getter.extracted_filename != None
          assert os.path.exists(self.file_getter.extracted_filename)
      
      def test_get_file_properties(self):
          get_file_properties = self.file_getter.get_file_properties()
          assert isinstance(get_file_properties, tuple)

          
      


