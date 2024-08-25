from odoo import models, fields, api


class AbstractOffer(models.Model):
    _name = 'abstract.model.offer'
    _description = 'Abstract.Offers'

    property_email = fields.Char(string='Email')
    property_phone = fields.Char(string="Phone Number")