from odoo import models, fields, api, _


class Property(models.Model):
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin','utm.mixin','website.published.mixin','website.seo.metadata']
    _description = "Real state properties"


    name = fields.Char(string="Name" , required=True)
    state = fields.Selection([('new', 'New'), ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'), ('sold', 'Sold'),('cancel','Cancelled')],
          default='new', string="State")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string= " Postcode")
    date_availability = fields.Date(string="Available Form")
    expected_price = fields.Float(string="Expected Price", tracking=True)
    selling_price = fields.Float(string="Selling Price")
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_price')
    beadrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Total Area(sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orintation", default='north')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    total_area = fields.Integer(string="Total Area", compute='_compute_total_area')
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    def action_accept(self):
        self.state='sold'

    def action_refused(self):
        self.state='cancel'
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')


    """ def action_client_action(self):
        return {
            'type': 'ir.actions.client',  # Make sure this line is correct
            #'tag': 'apps'  # Ensure the tag is correct and matches what Odoo expects
            'tag': 'display_notification',
            'params': {
                'title': _('Testing Client'),
                'type': 'success',
                'sticky': False
            }
        } """


    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer'
        }

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area
    

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    """#for Url Action 
    def action_url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://odoo.com',
            'target': 'self',
            #'target': 'new',
        } """
    
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Estate property - %s' % self.name
    
    def _compute_website_url(self):
        for rec in self:
            rec.website_url = "/properties/%s" % rec.ids

    def action_send_email(self):
        mail_template = self.env.ref('real_estate_ads.offer_mail_template')
        mail_template.send_mail(self.id, force_send=True)

    def _get_emails(self):
        emails = self.offer_ids.mapped('partner_email')
        return ''.join([email for email in emails if email])



class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Types'

    name = fields.Char(string="Name", required=True)




class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tags"


    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    