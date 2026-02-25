from pypdf import PdfReader, PdfWriter

class PDFOps:
    def __init__(self):
        self.file = "output2.pdf"
        self.output = r'C:\Users\Terry\PycharmProjects\PDFReorganizer\PDF\output.pdf'


    def set_file(self, file):
        self.file = file
        print(self.file)

    def rotate_pdf(self):
        file = self.file
        print(file)
        reader = PdfReader(self.file)
        writer = PdfWriter()
        angle = 90

        for page in reader.pages:
            # Rotate clockwise by 90, 180, or 270 degrees
            page.rotate(angle)
            writer.add_page(page)

        with open('output.pdf', "wb") as f:
            writer.write(f)

        print(f"Rotated {self.file} and saved as {self.output}")

    def reorder_pdf(self):
        reader = PdfReader(self.file)
        writer = PdfWriter()

        user_input = input("Enter items separated by comma." + f" Make sure that the list has {len(reader.pages)} pages: ")
        page_order = list(map(int, user_input.split(",")))
        if len(page_order) != len(reader.pages):
            print(page_order)
            input("error page does not match count")
            return

        page_order = [page - 1 for page in page_order]
        # Add pages to the output PDF in the specified order
        #l = list(range(len(reader.pages) - 1, -1, -1))
        for page_index in page_order:
            # Ensure the index is valid for the number of pages in the input PDF
            if 0 <= page_index < len(reader.pages):
                writer.add_page(reader.pages[page_index])
            else:
                print(f"Warning: Invalid page index {page_index}. Skipping.")

        # Write the reordered pages to a new file
        with open('output.pdf', 'wb') as writefile:
            writer.write(writefile)

        print(f"PDF successfully reordered and saved to {self.output}")
