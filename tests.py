import os
from challenge import FileGetter, StringSanitizer

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

          
      
class TestStringSanitizer:
    sanitizer = StringSanitizer()

    def test_remove_whitespace(self):
        string = ' pmweb'
        assert self.sanitizer.remove_whitespace(string) == 'pmweb'

    def test_phone_sanitize(self):
        string = ' +(55)119a A81-21%@23$5&&8'
        assert self.sanitizer.phone_sanitize(string) == '5511981212358'

    def test_to_ascii(self):
        string = ' 99 - São Paulo '
        assert self.sanitizer.to_ascii(string) == '99 - SAO PAULO'


