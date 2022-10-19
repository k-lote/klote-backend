from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

from ..models.allotment import Allotment, allotments_schema
from ..models.allotment_access import Allotment_access
from ..models.lot import Lot, lot_schema, lots_schema
from ..models.customer import Customer, customer_schema, customers_schema, CustomerHistory, customer_history_schema, customers_history_schema, Purchase, purchase_schema, purchase_schemas
from ..models.finances import Installment, installment_schema, installments_schema

#A4 = (210*mm,297*mm)

def mm(mm):
    return mm/0.352777

def gerarPDF(name, parcelas):
    #given
    customer = Customer(admin_id=1, address="Rua teste", phone1=81995167888, cpf=10029580404, name=name, email="teste@gmail.com", is_active=True, phone2=81995167888,cnpj="", corporate_name="")
    customer.id = 1
    loteamento = Allotment(name=name, cep=51160035, address="Rua do teste", img_url="", logo_url="")
    lote = Lot(allotment_id=loteamento.id, number=2, block="A", value=10000, is_available=False)
    valorParcela= lote.value/parcelas
    listParcelas = []
    for i in range(1,parcelas):
        listParcelas.append(Installment(value=valorParcela,date=datetime.now() ,installment_number=i, allotment_id=loteamento.id, lot_number=lote.number, is_paid = False))
        listParcelas[i-1].cod=i+313
    #then
    pdf = canvas.Canvas(f"static/{name}.pdf",pagesize=A4)
    eixo=mm(295)

    for parcela in listParcelas:
        gerarparcela(pdf,customer,loteamento,lote, eixo, parcela, parcelas)
        eixo-=mm(72)
        if parcela.installment_number%4 == 0:
            pdf.showPage()
            eixo=mm(295)
    pdf.save()
    file = open(f"static/{name}.pdf","rb")
    os.remove(f"static/{name}.pdf")

    return file

def gerarparcela(pdf,customer,loteamento,lote, eixo, parcela,parcelas):

    """
    Primeira parte da parcela
    """
    
    margem=mm(3)
    pdf.line(margem,eixo,mm(210)-margem,eixo)
    pdf.line(margem,eixo-mm(70),mm(210)-margem,eixo-mm(70))
    pdf.line(margem,eixo,margem,eixo-mm(70)) #vertical inicio
    pdf.line(mm(44.7),eixo,mm(44.7),eixo-mm(70)) #vertical primeira parte
    pdf.line(mm(210)-margem,eixo,mm(210)-margem,eixo-mm(70)) #vertical final
    titulos = ["( = ) Total Cobrado","( + ) Outros Acrécimos", "( + ) Multa / Mora", "( - ) Outros descontos", "( - ) Desconto"]
    pdf.setFont("Helvetica", 9)
    for i in range(5): #linha horizontais
        pdf.line(margem,eixo-mm(70-7*i),mm(44.7),eixo-mm(70-7*i)) 
        pdf.drawString(margem+mm(1),eixo-mm(69-7*i),titulos[i])
    titulosEsq= ["( = ) Valor do Documento",  "Parcela", "Documento"]
    titulosDir=["", "Vencimento", "Cliente"]
    inforDir=[f"R$ {parcela.value}", str(parcela.date).split()[0], customer.id]
    inforEsq=["", f"{parcela.installment_number}/{parcelas}", parcela.cod]
    for i in range(3):
        pdf.line(margem,eixo-mm(35-12*i),mm(44.7),eixo-mm(35-12*i)) 
        pdf.drawString(margem+mm(1),eixo-mm(27-12*i),titulosEsq[i])
        pdf.drawString(margem+mm(20),eixo-mm(27-12*i),titulosDir[i])
        pdf.setFont("Helvetica", 11)
        pdf.drawString(margem+mm(1),eixo-mm(33-12*i),str(inforEsq[i]))
        pdf.drawString(margem+mm(20),eixo-mm(33-12*i),str(inforDir[i]))
        pdf.setFont("Helvetica", 9)
    
    """
    Segunda parte da parcela
    """



    pdf.setFont("Helvetica", 12)
    pdf.drawString(margem+mm(45),eixo-mm(8),customer.name)
    #pdf.drawString(margem+mm(45),eixo-mm(70),f"{parcela}/{parcelas}")



    """
    Terceira parte da parcela
    """

    pdf.line(mm(210-44.7),eixo,mm(210-44.7),eixo-mm(56)) #vertical terceira parte
    titulos = ["( = ) Total Cobrado","( + ) Outros Acrécimos", "( + ) Multa / Mora", "( - ) Outros descontos", "( - ) Desconto"]
    pdf.setFont("Helvetica", 9)
    for i in range(5): #linha horizontais
        pdf.line(mm(210-44.7),eixo-mm(56-7*i),mm(210)-margem,eixo-mm(56-7*i)) 
        pdf.drawString(mm(210-44.7)+mm(1),eixo-mm(55-7*i),titulos[i])

    titulosEsq= ["( = ) Valor do Documento",  "Parcela"]
    titulosDir=["", "Vencimento"]
    inforDir=[f"R$ {parcela.value}", str(parcela.date).split()[0]]
    inforEsq=["", f"{parcela.installment_number}/{parcelas}"]
    deltaY=-mm(12)
    deltaX=mm(210-44.7)-margem
    for i in range(2):
        pdf.line(margem+deltaX,eixo-mm(35-12*i)-deltaY,mm(210)-margem,eixo-mm(35-12*i)-deltaY) 
        pdf.drawString(margem+mm(1)+deltaX,eixo-mm(27-12*i)-deltaY,titulosEsq[i])
        pdf.drawString(margem+mm(20)+deltaX,eixo-mm(27-12*i)-deltaY,titulosDir[i])
        pdf.setFont("Helvetica", 11)
        pdf.drawString(margem+mm(1)+deltaX,eixo-mm(33-12*i)-deltaY,str(inforEsq[i]))
        pdf.drawString(margem+mm(20)+deltaX,eixo-mm(33-12*i)-deltaY,str(inforDir[i]))
        pdf.setFont("Helvetica", 9)
    
    return pdf

if __name__ == '__main__':
    gerarPDF("Boleto.pdf", 50)
