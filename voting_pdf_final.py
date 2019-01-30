from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, PageTemplate, Table, Image, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from svglib.svglib import svg2rlg
from reportlab.lib.units import inch
import csv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF

pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif', 'FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerifItalic', 'FreeSerifItalic.ttf'))


styles=getSampleStyleSheet()
style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)

style_h = ParagraphStyle('He')
style_h.fontSize = 7
style_h.leading = style_h.fontSize*1.2
style_h.fontName = 'Helvetica'
style_h.alignment = TA_CENTER

Elements=[]

doc = BaseDocTemplate('voting_department_operation_research.pdf',showBoundary=1)

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


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_qr_code()
            self.draw_voter_index()
            self.draw_region_dep()
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(110*mm, 17*mm,
            "Page %d of %d" % (self._pageNumber, page_count))

    def draw_qr_code(self):
        drawing = svg2rlg("profile.svg")
        d = scale(drawing, scaling_factor=0.5)
        renderPDF.draw(d, self,170*mm,272*mm)
    def draw_region_dep(self):
        self.setFont("Helvetica", 7)
        p1 = Paragraph('Region Type: <b>Country</b>', style_h)
        p2 = Paragraph('Region Name: <b>Peace</b>', style_h)
        p3 = Paragraph("Department Name: <b>Research</b>", style_h)
        p4 = Paragraph("Department Code: <b>RD</b>", style_h)
        (a1w, a1h) = (a2w, a2h) = (a3w, a3h) = (a4w, a4h) = doc.pagesize
        w1, h1 = p1.wrap(a1w,a1h)
        w2, h2 = p2.wrap(a2w,a2h)
        w3, h3 = p3.wrap(a3w,a3h)
        w4, h4 = p4.wrap(a4w,a4h)
        p1.drawOn(self, 0, a1h-30)
        p2.drawOn(self, 0, a2h-40)
        p3.drawOn(self, 0, a3h-50)
        p4.drawOn(self, 0, a4h-60)
    def draw_voter_index(self):
        self.setFont("Helvetica", 7)
        self.drawString(25*mm, 275*mm,
            "Voter Index: ________________")














def setTags():
        doc.canv.setAuthor("Amiya Behera")
        doc.canv.setTitle("Evolutionary Democracy Voting")
doc.beforeDocument = setTags



#Two Columns
frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')

drawing = svg2rlg("square.svg")

p2 = scale(drawing, scaling_factor=0.1)

style_p = ParagraphStyle('A')
style_p.fontSize = 7
style_p.leading = style_p.fontSize*1.2
style_p.fontName = 'FreeSansBold'
style_p.alignment = TA_LEFT

style_s = ParagraphStyle('S')
style_s.fontSize = 18
style_s.fontName = 'FreeSerif'

style_sm = ParagraphStyle('C')
style_sm.fontSize = 6
style_sm.leading = style_sm.fontSize*1.2
style_sm.fontName = 'FreeSansBold'
style_sm.alignment = TA_LEFT



x = 1
with open('vote_names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            p0 = Paragraph("RD-" + str(x) + ". " , style_sm)
            p1 = Paragraph('<b>' + row['name'] + " </b>",style_p)
            data = [[p0, p1, p2]]
            tbl = Table(data, colWidths=[0.5*inch, None, 0.4*inch])
            st = TableStyle([
                    ('ALIGN', (1, 0), (1, 0), "LEFT"),
                    ('ALIGN', (2, 0), (2, 0), "RIGHT"),
                ])
            tbl.setStyle(st)
            Elements.append(tbl)
            x = x + 1
doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2], ), ])


#start the construction of the pdf
doc.build(Elements, canvasmaker=NumberedCanvas)