from pypdf import PdfReader, PdfWriter
import os
import re
from pathlib import Path
import sys
from collections import Counter

class PDFOps:
    def __init__(self):
        self.file = None
        self.output = None
        if getattr(sys, 'frozen', False):
            # This block is executed if the script is running inside a PyInstaller/similar executable
            print("Running in a standalone executable (.exe)")
            print(f"Executable path: {sys.executable}")
            current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
            file_path = os.path.abspath(current_dir)
            self.output = file_path
        else:
            # This block is executed if the script is running as a normal .py file
            print("Running as a Python script (.py)")
            print(f"Interpreter path: {sys.executable}")
            self.output = os.path.dirname(os.path.realpath(__file__))

    def Continue(self):
        input("Press Any key to continue...")

    def set_file(self, file):
        self.file = file
        self.output += "\output.pdf"
        if os.access(self.file, os.R_OK):
            print(f"File location: {file} is readable")
        else:
            print(f"File Location: {file} is not readable")

        if os.access(self.file, os.W_OK):
            print(f"File location: {file} is writable")
        else:
            print(f"File location: {file} is not writable")
        try:
            os.chmod(self.output, 0o600)
        except Exception as e:
            print(f"{e}" + " Please note that this means that the file will be created and that it does not exist yet.")
            self.Continue()
        if os.access(self.output, os.R_OK):
            print(f"File location: {self.output} is readable")
        else:
            print(f"File Location: {self.output} is not readable")

        if os.access(self.output, os.W_OK):
            print(f"File location: {self.output} is writable")
        else:
            print(f"File location: {self.output} is not writable")

        self.Continue()



    def rotate_pdf(self, angle = 90):
        reader = PdfReader(self.file)
        writer = PdfWriter()

        if angle not in [90, 180, 270, 0]:
            print(f"the program cannot be executed with this angle: {angle}. Program will quit.")
            self.Continue()
            quit()

        for page in reader.pages:
            # Rotate clockwise by 90, 180, or 270 degrees
            page.rotate(angle)
            writer.add_page(page)
        try:
            with open(self.output, "wb") as f:
                writer.write(f)
                print(f"Successfully created file: {self.output}")
        except PermissionError as e:
            print(f"Permission denied: {e}")
            print("Try running the script as an administrator or saving to a different directory.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


        print(f"Rotated {self.file} and saved as {self.output}")
        self.Continue()

    def reorder_pdf(self):
        reader = PdfReader(self.file)
        writer = PdfWriter()

        current_order = list(range(len(reader.pages)))
        print(f"Current order of file pages: {[page + 1 for page in list(range(len(reader.pages)))]}")

        user_input = input("Enter items separated by comma." + " You may type (r) to just reverse the order of pages. "
                           + f" Make sure that the list has {len(reader.pages)} pages: ")

        page_order = None
        if user_input == "r":
            page_order = list(range(len(reader.pages) - 1, -1, -1))
        else:
            page_order = list(map(int, re.split(r'[,\\s]+', user_input)))
            if 0 not in page_order:
                page_order = [page - 1 for page in page_order]
            if len(page_order) != len(reader.pages):
                print(f"match number of pages: {len(page_order) == len(reader.pages)}")
                print(page_order)
                print(current_order)
                input("Error page list does not match count. Program will quit")
                quit()
            if Counter(page_order) != Counter(current_order):
                print(f"List match: {Counter(page_order) == Counter(current_order)}")
                print(page_order)
                print(current_order)
                input("Error page list does not contain all values. Program will quit")
                quit()


        # Add pages to the output PDF in the specified order
        for page_index in page_order:
            # Ensure the index is valid for the number of pages in the input PDF
            if 0 <= page_index < len(reader.pages):
                writer.add_page(reader.pages[page_index])
            else:
                print(f"Warning: Invalid page index {page_index}. Skipping.")

        # Write the reordered pages to a new file
        try:
            with open(self.output, "wb") as f:
                writer.write(f)
                print(f"Successfully created file: {self.output}")
        except PermissionError as e:
            print(f"Permission denied: {e}")
            print("Try running the script as an administrator or saving to a different directory.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print(f"PDF successfully reordered and saved to {self.output}")
        self.Continue()
