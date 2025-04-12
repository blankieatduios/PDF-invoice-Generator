from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import json
from datetime import datetime

class InvoiceGenerator:
    def __init__(self, data):
        self.data = data
        self.styles = getSampleStyleSheet()
    
    def create_invoice(self, output_filename):
        doc = SimpleDocTemplate(output_filename, pagesize=letter)
        elements = []
        
        # Header
        elements.append(Paragraph(f"Invoice #{self.data['invoice_number']}", 
                                self.styles['Heading1']))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", 
                                self.styles['Normal']))
        elements.append(Paragraph("", self.styles['Normal']))
        
        # Client Info
        elements.append(Paragraph("Bill To:", self.styles['Heading2']))
        elements.append(Paragraph(self.data['client_name'], 
                                self.styles['Normal']))
        elements.append(Paragraph(self.data['client_address'], 
                                self.styles['Normal']))
        elements.append(Paragraph("", self.styles['Normal']))
        
        # Items Table
        table_data = [['Item', 'Quantity', 'Unit Price', 'Total']]
        total = 0
        
        for item in self.data['items']:
            item_total = item['quantity'] * item['unit_price']
            total += item_total
            table_data.append([
                item['description'],
                str(item['quantity']),
                f"${item['unit_price']:.2f}",
                f"${item_total:.2f}"
            ])
        
        # Add total row
        table_data.append(['', '', 'Total:', f"${total:.2f}"])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)

def main():
    # Sample invoice data
    invoice_data = {
        'invoice_number': '2025001',
        'client_name': 'John Doe',
        'client_address': '123 Main St\nNew York, NY 10001',
        'items': [
            {
                'description': 'Web Development',
                'quantity': 10,
                'unit_price': 150.00
            },
            {
                'description': 'Server Maintenance',
                'quantity': 5,
                'unit_price': 100.00
            }
        ]
    }
    
    generator = InvoiceGenerator(invoice_data)
    generator.create_invoice('invoice.pdf')

if __name__ == '__main__':
    main()
