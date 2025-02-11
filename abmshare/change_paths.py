import os
import re
import json
import jsbeautifier
import yaml
import pandas as pd
from pathlib import Path

class RecursiveChangePaths():

  def __init__(self, directory, pattern, replacement):
    self.directory = directory
    self.pattern = pattern
    self.replacement = replacement
    # Call it
    self.process_directory(self.directory, self.pattern, self.replacement)
  # Function to replace a pattern in a string
  def replace_pattern(self,content, pattern, replacement):
      return re.sub(pattern, replacement, content)

  # Function to process a file based on its extension
  def process_file(self,file_path, pattern, replacement):
      try:
          # Read and process CSV files
          if file_path.suffix == ".csv":
              df = pd.read_csv(file_path)
              df.replace(pattern, replacement, regex=True, inplace=True)
              df.to_csv(file_path, index=False)
              print(f"Processed CSV file: {file_path}")

          # Read and process Excel files
          elif file_path.suffix in [".xlsx", ".xls"]:
              df = pd.read_excel(file_path)
              df.replace(pattern, replacement, regex=True, inplace=True)
              df.to_excel(file_path, index=False)
              print(f"Processed Excel file: {file_path}")

          # Read and process JSON files
          elif file_path.suffix == ".json":
              with open(file_path, "r", encoding="utf-8") as file:
                  data = json.load(file)
              modified_data = json.dumps(data)
              modified_data = self.replace_pattern(modified_data, pattern, replacement)
              options = jsbeautifier.default_options()
              options.indent_size = 2
              pretty_json=jsbeautifier.beautify(json.dumps(modified_data), options)
              with open(file_path, "w", encoding="utf-8") as file:
                  file.write(pretty_json)
              print(f"Processed JSON file: {file_path}")

          # Read and process YAML files
          elif file_path.suffix in [".yaml", ".yml"]:
              with open(file_path, "r", encoding="utf-8") as file:
                  data = yaml.safe_load(file)
              modified_data = yaml.dump(data)
              modified_data = self.replace_pattern(modified_data, pattern, replacement)
              with open(file_path, "w", encoding="utf-8") as file:
                  file.write(modified_data)
              print(f"Processed YAML file: {file_path}")

      except Exception as e:
          print(f"Error processing file {file_path}: {e}")

  # Function to recursively traverse directories and process files
  def process_directory(self,directory, pattern, replacement):
      if not os.path.isdir(directory):
          print(f"Error: Directory '{directory}' does not exist.")
          return
      for root, _, files in os.walk(directory):
          for file in files:
              file_path = Path(root) / file
              if file_path.suffix in [".csv", ".xlsx", ".xls", ".json", ".yaml", ".yml"]:
                  self.process_file(file_path, pattern, replacement)