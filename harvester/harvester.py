import os
from typing import Optional, Type
from crawler import crawler
from parser import Parser
from file_group import File, FileGroup, SuperGroup


def harvester(path: str, verbose: Optional[bool] = False) -> Type[SuperGroup]:
   """
   This function harvests metadata from files under a given path by using parsers that parse files with different filetypes


   Args:
       path: Base directory for metadata harvesting
       verbose: A boolean indicating if messages should be generated regarding unparsed file(s) and filetype(s) in the given path


   Returns:
       all_file_groups: An instance of SuperGroup that contains all groups of files parsed for metadata and harvested metadata
   """
   if verbose:
       print(f"Start havesting metadata from files under the given path {target_path}\n")
  
   # Find all files under the given path
   file_dict = crawler(path)
   # Create an instance of Parser class
   parser = Parser()


   # Create a dictionary to hold the filetypes that has no corresponding parsers
   unparsed_file_type_dict = {}


   # Create an instance of SuperGroup class to hold all parsed files grouped based on file_types.
   all_file_groups = SuperGroup(name="all parsed file groups", groups=[])
      
   # Use file parsers to extract metadata from files
   if file_dict:
       for file_type in file_dict:
           file_type_parser_name = "parse_" + file_type
          
           # Check if parser exists for the specific file_type
           file_type_parser = getattr(parser, file_type_parser_name, None)
           # Use parser to parse the files of the specfic file_type if exists
           if file_type_parser:        
               file_group_name = file_type + " files"
               # Create an instance of FileGroup for the specific file_type
               # and add it to SuperGroup instance's list of groups
               file_group_instance = FileGroup(name=file_group_name, files=[])
               all_file_groups.groups.append(file_group_instance)
              
               for file in file_dict[file_type]:
                   file_name = os.path.split(file)[1]
                   # Use parser to extract metadata from file
                   metadata = file_type_parser(file)
                   # Create an instance of File and append it to the corrsponding FileGroup's list of files
                   file_object = File(name=file_name, path=file, metadata=metadata)
                   file_group_instance.files.append(file_object)
      
           else:
               unparsed_file_type_dict[file_type] = file_dict[file_type]          
   else:
       if verbose:
           print("No file is found under the given path\n")   


   # Print out information regarding unparsed file_types and files if verbose is True
   if unparsed_file_type_dict:
       unparsed_file_types = list(unparsed_file_type_dict.keys())
       unparsed_files = [file for sublist in unparsed_file_type_dict.values() for file in sublist]
       if verbose:
           print(f"Please note that currently there are no parsers to parse {', '.join(unparsed_file_types[:-1])} and {unparsed_file_types[-1]} files found under the given path.\n")
           print(f"List of unparsed files: {unparsed_files}\n\n")
      
   return all_file_groups






if __name__ == "__main__":
  
   print("----- A simple example of using harvester to extract metadata from all files in a given directory ---- \n")
  
   # Define the target path that contains files for metadata harvesting
   target_path = os.path.join(os.path.dirname(os.getcwd()), "Example")
  
   # Use harvester to parse files and extract metadata
   all_file_groups = harvester(target_path, True)
   print("---*** Matadata harvester output ***---\n")
   print(all_file_groups.yaml())
   print(f"--- Tree visulization of metadata harvested---\n")
   all_file_groups.visualize_tree()
   print("\n")
  
   #Export output from metadata harvester into a json file
   with open("harvester_output.json", "w") as f:
       f.write(all_file_groups.json())

