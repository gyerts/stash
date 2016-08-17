from report_generator_lib.report_views.xlsx_utils import *
import xlsxwriter
import json

height = dict()
line_height = 11


green_format = {
    'bold':     True,
    'border':   6,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#D7E4BC',
}
red_format = {
    'bold':     True,
    'border':   6,
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': 'orange',
}

def get_content_height(content):
    return line_height * len(content)


def get_height(line, content):
    if line in height:
        content_height = get_content_height(content)
        if content_height > height[line]:
            height[line] = content_height
    else:
        height[line] = line_height * len(content)
    return height[line]


def stash_report_view(path):

    data = open("data.json").read()
    lines = json.loads(data)

    xlsx = xlsxwriter.Workbook(path)

    formatHeader = xlsx.add_format(XlsxCellStyle.header)
    formatNormal = xlsx.add_format(XlsxCellStyle.normal)
    formatGreen = xlsx.add_format(green_format)
    formatRed = xlsx.add_format(red_format)

    # step 1: init work sheet
    generalTab = xlsx.add_worksheet("General")

    row = 0
    col = 0

    # step 2: headers
    header = ["Change list", "Date", "Review", "Reviewed", "Author", "Domain", "State",
              "Reviewers", "Files", "Formats", "Comments", "Comments text", "Time spent"]

    for i in range(len(header)):
        generalTab.write(row, col + i, header[i], formatHeader)

    row += 1


    # step 3: main data
    for line in lines:
        generalTab.write(row, col + 0,   line["change"], formatNormal)

        generalTab.write(row, col + 1,   line["date"], formatNormal)

        generalTab.write(row, col + 2,   line["review"], formatNormal)

        if line["reviewed"] == "True":
            generalTab.write(row, col + 3,   line["reviewed"], formatGreen)
        else:
            generalTab.write(row, col + 3,   line["reviewed"], formatRed)

        generalTab.write(row, col + 4,   line["author"], formatNormal)

        generalTab.write(row, col + 5,   ",\n".join(line["domain"]), formatNormal)
        generalTab.set_row(row, get_height(row, line["domain"]))

        if line["state"] == "Reviewed":
            generalTab.write(row, col + 6,   line["state"], formatGreen)
        else:
            generalTab.write(row, col + 6,   line["state"], formatRed)

        generalTab.write(row, col + 7,   ",\n".join(line["reviewers"]), formatNormal)
        generalTab.set_row(row, get_height(row, line["reviewers"]))

        generalTab.write(row, col + 8,   ",\n".join(line["files"]), formatNormal)
        generalTab.set_row(row, get_height(row, line["files"]))

        generalTab.write(row, col + 9,   ",\n".join(line["formats"]), formatNormal)
        generalTab.set_row(row, get_height(row, line["formats"]))

        generalTab.write(row, col + 10,  line["comments"], formatNormal)

        generalTab.write(row, col + 11,  ",\n".join(line["comments_text"]), formatNormal)
        generalTab.set_row(row, get_height(row, line["comments_text"]))

        generalTab.write(row, col + 12,  line["time_spent"], formatNormal)

        row += 1

    generalTab.autofilter(0, 0, row, 12)

    generalTab.set_column(0, 0, 36)    # Change list
    generalTab.set_column(1, 1, 18)    # Date
    generalTab.set_column(2, 2, 40)    # Review
    generalTab.set_column(3, 3, 4)     # Reviewed
    generalTab.set_column(4, 4, 10)    # Author
    generalTab.set_column(5, 5, 10)    # Domain
    generalTab.set_column(6, 6, 15)    # State
    generalTab.set_column(7, 7, 15)    # Reviewers
    generalTab.set_column(8, 8, 50)    # Files
    generalTab.set_column(9, 9, 5)     # Formats
    generalTab.set_column(10, 10, 3)   # Comments
    generalTab.set_column(11, 11, 40)  # Comments text
    generalTab.set_column(12, 12, 10)  # Time spent

    xlsx.close()

stash_report_view("output.xlsx")
