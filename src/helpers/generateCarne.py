from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
#A4 = (210*mm,297*mm)

def mm(mm):
    return mm/0.352777

def gerarPDF(name, parcelas):
    pdf = canvas.Canvas(f"static/{name}.pdf",pagesize=A4)
    eixo=mm(297)

    for parcela in range(1,parcelas+1):
        gerarparcela(pdf,name, eixo, parcela, parcelas)
        eixo-=mm(74)
        if parcela%4 == 0:
            pdf.showPage()
            eixo=mm(297)
    pdf.save()
    file = open(f"static/{name}.pdf","rb")
    return file

def gerarparcela(pdf, cliente, eixo, parcela, parcelas):
    #pdf.drawImage("model.png",0,eixo,height=mm(74),width=mm(210))
    margem=mm(2)
    pdf.line(margem,eixo-mm(74),mm(210)-margem,eixo-mm(74))
    pdf.drawString(margem,eixo-mm(8),cliente)
    pdf.drawString(margem,eixo-mm(70),f"{parcela}/{parcelas}")
    
    return pdf

if __name__ == '__main__':
    gerarPDF("Boleto.pdf", 50)
