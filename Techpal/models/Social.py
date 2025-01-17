from odoo import models, fields, api
import base64

class Social(models.Model):
    _name = 'social'
    _description = 'Social Marketing Techpal'
    _order = 'sequence'

    name = fields.Char(string="Nom de la campagne", required=True)
    date = fields.Date(string="Date de la campagne", required=True)
    type = fields.Selection([('video', 'video'), ('image', 'image'), ('carousel','Carousel')], string="Type de la campagne", required=True)
    content = fields.Text(string="Contenu de la campagne", required=True)
    tags = fields.Many2many('social.tags', string="Tags")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=1)
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Pièces Jointes'
    )
    stages = fields.Selection([
        ('nouveau' , 'Nouveau') , 
        ('programme', 'Programme') , 
        ('design', 'Design') , 
        ('envoye', 'Envoyé') 
    ] , default="nouveau" , group_expand='_group_expand_states' , track_visibility='always')

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).stages.selection]

class SocialTags(models.Model):
    _name = 'social.tags'
    _description = 'Social Tags for Marketing'

    name = fields.Char(string="Nom du tag", required=True)


class SocialStage(models.Model):
    _name = 'social.stage'
    _description = 'Stages for Social Campaigns'

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
