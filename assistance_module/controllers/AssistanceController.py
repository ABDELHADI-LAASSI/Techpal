from odoo import http
from odoo.http import request, route, content_disposition
import re
import base64

class AssistanceController(http.Controller):
    @http.route('/my/demande_assistance', type='http', auth='user', website=True)
    def custom_assistance_table(self, **kwargs):
        success = kwargs.get('success', False)
        values = {
            'success_message': "la demande d'assistance soumise avec succès!" if success else False
        }
        return request.render('assistance_module.custom_assistance_table_template', values)

    @http.route('/my/demande_assistance/form', type='http', auth='user', website=True)
    def custom_assistance_form(self, **kwargs):
        user = request.env.user
        company_name = user.partner_id.name
        company_email = user.partner_id.email
        return request.render('assistance_module.custom_assistance_form_template', {
            'company_name': company_name,
            'company_email': company_email
        })


    @http.route('/my/demande_assistance/<int:assistance_id>', type='http', auth='user', website=True)
    def individual_assistance(self, assistance_id, **kwargs):
        # Get the assistance request by its ID
        assistance = request.env['assistance'].sudo().browse(assistance_id)
        success = kwargs.get('success', False)

        # If assistance doesn't exist, return 404
        if not assistance.exists():
            request.redirect('/my/demande_assistance?success=True')

        # Pass the assistance record to the template
        values = {
            'assistance': assistance,
            'success_message': "Retour d'information soumis avec succès!" if success else False
        }
        return request.render('assistance_module.individual_assistance_template', values)

    @http.route('/my/custom_form/submit', type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def submit_custom_form(self, **post):
        # Extract submitted form data
        user = request.env.user  # Current logged-in user
        company_name = user.partner_id.id  # Partner record ID (linked company)
        objet = post.get('objet')
        ticket_type = post.get('ticket_type')
        type_probleme = post.get('type_probleme')
        description = post.get('description')
        priority = post.get('priority')

        # Handle attachments
        attachment_files = request.httprequest.files.getlist('attachments')

        print('attachment_files', attachment_files)
        attachment_ids = []

        for attachment in attachment_files:
            data = attachment.read()  # Read file content
            attachment_id = request.env['ir.attachment'].sudo().create({
                'name': attachment.filename,
                'type': 'binary',
                'datas': base64.b64encode(data),
                'res_model': 'assistance',  # Link to your model
            }).id
            attachment_ids.append(attachment_id)

        print('attachment_ids', attachment_ids)

        # Create a record in the 'assistance' model
        request.env['assistance'].sudo().create({
            'company_name': company_name,
            'objet': objet,
            'ticket_type': ticket_type,
            'type_probleme': type_probleme,
            'description': description,
            'priority': priority,
            'attachment_ids': [(6, 0, attachment_ids)],  # Link attachments
        })

        # Redirect to main page
        return request.redirect('/my/demande_assistance?success=True')


    def _show_report(self, model, report_type, report_ref, download=False):
        if report_type not in ('html', 'pdf', 'text'):
            raise UserError(_("Invalid report type: %s", report_type))

        ReportAction = request.env['ir.actions.report'].sudo()

        if hasattr(model, 'company_id'):
            if len(model.company_id) > 1:
                raise UserError(_('Multi company reports are not supported.'))
            ReportAction = ReportAction.with_company(model.company_id)

        method_name = '_render_qweb_%s' % (report_type)
        report = getattr(ReportAction, method_name)(report_ref, list(model.ids), data={'report_type': report_type})[0]
        headers = self._get_http_headers(model, report_type, report, download)
        return request.make_response(report, headers=list(headers.items()))

    def _get_http_headers(self, model, report_type, report, download):
        headers = {
            'Content-Type': 'application/pdf' if report_type == 'pdf' else 'text/html',
            'Content-Length': len(report),
        }
        if report_type == 'pdf' and download:
            filename = "%s.pdf" % (re.sub(r'\W+', '-', model._get_report_base_filename()))
            headers['Content-Disposition'] = content_disposition(filename)
        return headers
    
    @http.route('/my/assistance/download_report/<int:assistance_id>', type='http', auth='user', website=True)
    def download_report(self, assistance_id, **kwargs):
        assistance = request.env['assistance'].sudo().browse(assistance_id)
        if not assistance.exists():
            return request.not_found()

        return self._show_report(
            model=assistance,
            report_type="pdf",
            report_ref="assistance_module.assistance_template",
            download=True
        )

    @http.route('/my/assistance/add_feedback', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def add_feedback(self, assistance_id, client_feedback, **kwargs):
        # Ensure the assistance ID is valid
        print("===============",assistance_id)
        assistance = request.env['assistance'].sudo().browse(int(assistance_id))
        if not assistance.exists():
            return request.not_found()

        # Update the feedback field
        assistance.client_feedback = client_feedback

        return request.redirect('/my/demande_assistance/%s' % assistance_id + '?success=True')

