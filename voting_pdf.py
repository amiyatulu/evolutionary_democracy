from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, PageTemplate, Table, Image, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from svglib.svglib import svg2rlg
from reportlab.lib.units import inch
import csv





styles=getSampleStyleSheet()
style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
Elements=[]

doc = BaseDocTemplate('voting_department_research.pdf',showBoundary=1)

def setTags():
        doc.canv.setAuthor("Amiya Behera")
        doc.canv.setTitle("Evolutionary Democracy Voting")
doc.beforeDocument = setTags


#Two Columns
frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')

drawing = svg2rlg("square.svg")
def scale(drawing, scaling_factor):
    """
    Scale a reportlab.graphics.shapes.Drawing()
    object while maintaining the aspect ratio
    """
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing
p2 = scale(drawing, scaling_factor=0.1)

style_p = ParagraphStyle('A')
style_p.fontSize = 7
style_p.leading = style_p.fontSize*1.2
style_p.fontName = 'Courier'
style_p.alignment = TA_LEFT


x = 1
with open('vote_names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            p0 = Paragraph(str(x) + ". " , style_p)
            p1 = Paragraph('<b>' + row['name'] + " </b>",style_p)
            data = [[p0, p1, p2]]
            tbl = Table(data, colWidths=[0.5*inch, None, None])
            st = TableStyle([
                    ('ALIGN', (1, 0), (1, 0), "LEFT"),
                    ('ALIGN', (2, 0), (2, 0), "RIGHT"),
                ])
            tbl.setStyle(st)
            Elements.append(tbl)
            x = x + 1
doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])


#start the construction of the pdf
doc.build(Elements)