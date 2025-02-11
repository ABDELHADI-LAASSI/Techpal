from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class Assistance(models.Model):
    _name = "assistance"
    _description = "Assistance"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add chatter functionality
    _order = 'sequence'

    #Main fields
    name = fields.Char(default="Nouveau", readonly=True)
    objet = fields.Text(string="Objet")
    company_name = fields.Many2one(
        'res.partner', 
        string="Nom de l'entreprise", 
        domain=[('is_company', '=', True)]  # Only show companies
    )
    ticket_type = fields.Selection([
        ('incident', 'Incident'),
        ('demande', 'Demande'),
    ], string="Type du ticket", default="incident")

    email = fields.Char('Courriel', related="company_name.email", readonly=True, store=True)
    phone = fields.Char('Téléphone', related="company_name.phone", readonly=True, store=True)
    adress = fields.Char('Adress', related="company_name.street", readonly=True, store=True)

    assistance_tags = fields.Many2many('assistance.tags', string="Étiquettes")
    time_to_create = fields.Html(string="Time to Create", compute="_compute_time_to_create")

    # Priority and Dates
    priority = fields.Selection([
        ('P5', 'Minime (P5)'),
        ('P1', 'Critique (P1)'),
        ('P2', 'Haute (P2)'),
        ('P3', 'Moyenne (P3)'),
        ('P4', 'Basse (P4)')
    ], string="Priorité", default='P3')
    creation_date = fields.Datetime(string="Date de création", default=fields.Datetime.now)
    end_date = fields.Datetime(string="Date de fin", readonly=True)
    article = fields.Char(string="Article")

    # report fields
    materiel = fields.Text(string="Objet")
    garantie = fields.Char(string="")
    nature_de_contract = fields.Selection([
        ('infogerance','infogérance'),
    ],string="", default="infogerance")
    diagnostic = fields.Text(string="")
    traveaux_realises = fields.Text(string="")
    date_intervention = fields.Datetime(string="")
    date_fin_intervention = fields.Datetime(string="")
    duree_intervention = fields.Char(string="Durée d'intervention", compute="_compute_duree_intervention", store=True)
    deplacement_km = fields.Float(string="")
    remarque = fields.Text(string="")
    technicien = fields.Many2one( 'res.partner',  string="")


    # Additional fields
    type_probleme = fields.Selection([
        ('internet','Internet'),
        ('resaux','Résaux'),
        ('wifi','Wifi'),
        ('pc','Pc'),
        ('imprimante','Imprimante'),
        ('telephone','Telephone'),
        ('camera','Camera'),
    ], default="internet")
    description = fields.Text(string="Description du problème")
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Pièces Jointes'
    )
    client_feedback = fields.Text(string="Retour client")

    stages = fields.Selection([
        ('nouveau', 'Nouveau'),
        ('affecte', 'Affecté'),
        ('pris_charge', 'Pris en charge'),
        ('fait', 'Résolu'),
        ('closed', 'Annulé')
    ], string="Stages", default="nouveau", group_expand='_group_expand_states')
    last_stage_change = fields.Datetime(string="Dernier Changement d'Étape", default=fields.Datetime.now)
    previous_stage = fields.Char(string="Previous Stage", readonly=True)

    sequence = fields.Integer(default=1)

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in self._fields['stages'].selection]

    @api.constrains('date_intervention', 'date_fin_intervention')
    def _check_date_intervention(self):
        for record in self:
            if record.date_fin_intervention and record.date_intervention:
                if record.date_fin_intervention < record.date_intervention:
                    raise ValidationError(
                        "La date de fin d'intervention ne peut pas être antérieure à la date d'intervention."
                    )


    @api.depends('date_intervention', 'date_fin_intervention')
    def _compute_duree_intervention(self):
        for record in self:
            if record.date_intervention and record.date_fin_intervention:
                duration = record.date_fin_intervention - record.date_intervention
                total_minutes = int(duration.total_seconds() / 60)
                hours = total_minutes // 60
                minutes = total_minutes % 60

                if hours > 0:
                    record.duree_intervention = f"{hours}h {minutes}min" if minutes else f"{hours}h"
                else:
                    record.duree_intervention = f"{minutes}min"
            else:
                record.duree_intervention = ""

    @api.depends('creation_date')
    def _compute_time_to_create(self):
        for record in self:
            if record.creation_date:
                now = datetime.now()
                diff_minutes = (now - record.creation_date).total_seconds() / 60
                if diff_minutes > 15:
                    css_class = "minutes-red"
                else:
                    css_class = "minutes"
                min_word = 'Min'
                if diff_minutes <= 1:
                    min_word = 'minute'
                # Wrap the value in an HTML tag with a class
                record.time_to_create = f'<span class="{css_class}">{int(diff_minutes)} {min_word}</span>'
            else:
                record.time_to_create = '<span class="minutes">0 Min</span>'

    @api.model
    def write(self, vals):
        if 'stages' in vals:  # Check if 'stages' field is being updated
            for record in self:
                # Capture the current stage as the previous stage before updating
                previous_stage = record.stages
                time_now = datetime.now()

                if record.last_stage_change:  # Ensure there's a previous change time
                    time_spent = time_now - record.last_stage_change
                    hours, remainder = divmod(time_spent.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)

                    # Post a message in the chatter about the transition
                    record.message_post(
                        body=(
                            f"Le ticket a quitté l'étape {previous_stage} "
                            f"pour l'étape {vals['stages']} après "
                            f"{int(hours)} heures et {int(minutes)} minutes."
                        )
                    )

                # Update 'last_stage_change' and 'previous_stage' for the record
                vals['last_stage_change'] = time_now
                vals['previous_stage'] = previous_stage
                self.creation_date = time_now

                 # Set 'end_date' if transitioning to specific stages
                if vals['stages'] in ['fait', 'closed']:
                    vals['end_date'] = time_now

        return super(Assistance, self).write(vals)



    def send_email(self, email_to):
        template = self.env.ref('assistance_module.asistance_notification_template')
        template.email_to = email_to
        template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):
        res = super(Assistance, self).create(vals)
        if res.name == 'Nouveau':
            res.name = self.env['ir.sequence'].next_by_code('assistance_seq.')
        self.send_email('bbe@techpalservices.com')
        self.send_email('techpalservices@gmail.com')
        return res
    
    def to_cancelled(self):
        self.stages = "pris_charge"
    
    def to_fait(self):
        self.stages = "fait"
    def to_closed(self):
        self.stages = "closed"
    def to_encours(self):
        self.stages = "affecte"

    def _get_report_base_filename(self):
        return self.name

    

class AssistanceTags(models.Model):
    _name = 'assistance.tags'
    _description = 'Assistance Tags'

    name = fields.Char(string="Nom du tag", required=True)
