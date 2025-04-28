from xlsxwriter import worksheet
from odoo import http
from odoo.http import request
import io
import xlsxwriter


class Xlsx_report(http.Controller):

    @http.route('/vente/excel/report', type='http', auth='user')
    def download_excel_report(self):
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Ventes')

        header_format = workbook.add_format({'bold': True, 'border': True})

        headers = ['Entreprise', 'ICE', 'Vente total HT', 'Vente total TTC']

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        workbook.close()
        output.seek(0)

        file_name = 'SaleState.xlsx'

        return request.make_response(
        output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
            ]
        )
