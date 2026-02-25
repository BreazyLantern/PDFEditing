import sys
from dbm import error
from PDF_Functions import PDFOps
# Define the desired page order using 0-based indices.
# Example: [2, 0, 1, 3] would make the 3rd page the 1st, the 1st page the 2nd, etc.
#page_order = [5,6,0,1,2,3,4] # Adjust this list to your specific reordering needs


input_pdf_path = None
try:
    input_pdf_path = sys.argv[1:]
except error:
    print("No file dropped")

pdf = PDFOps()
pdf.set_file(input_pdf_path[0])

print("what operation would you like: (r) to rotate docs, or (re) to renumber doc order, (q) to quit")
operation = input()

if operation == "r":
    try:
        pdf.rotate_pdf(int(input("Input 0, 90, 180, 270: ")))
    except Exception as error_log:
        input(error_log)
        quit()
elif operation == "re":
    pdf.reorder_pdf()
else:
    input("good bye")