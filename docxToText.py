import glob
import os


#create dir obj to grab all docx paths 
directory = glob.glob('melinda_recipes_docx_files/**/*.docx', recursive=True)
for name in(directory):
    print(name)
