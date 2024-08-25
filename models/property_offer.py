from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    name = fields.Char(string="Description", compute='_compute_name')
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    partner_email = fields.Char(string="Customer Email", related='partner_id.email')
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)  # Default validity period
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline', store=True)
    creation_date = fields.Date(string="Create Date", default=fields.Date.context_today)  # Use today's date as default

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False  # Explicitly set to False if no creation_date or validity

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.context_today(self)
        return super(PropertyOffer, self).create(vals)
    
    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })
        self.status = 'accepted'

    def _validate_accepted_offer(self):
        existing_offer = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if existing_offer:
            raise ValidationError(_("An offer has already been accepted for this property."))

    def action_decline_offer(self):
        self.status = 'refused'
        if all(offer.status == 'refused' for offer in self.property_id.offer_ids):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    #server action
    def extend_offer_deadline(self):
        activ_ids = self._context.get('active_ids',[])
        if activ_ids:
            offer_ids = self.env['estate.property.offer'].browse(activ_ids)
            for offer in offer_ids:
                offer.validity = 10

    #Scheduled Action
    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
                offer.validity = offer.validity + 1
        
    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline and rec.deadline <= rec.creation_date:
                raise ValidationError(_("The deadline cannot be before the creation date."))


    # Example of a model cleaning method that deletes refused offers.
    """ @api.model
    def _clean_offers(self):
        refused_offers = self.search([('status', '=', 'refused')])
        refused_offers.unlink() """


    """ @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline cannot be before creation date"))
             """
   


    """ def write(self, vals):
        print(vals)
        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
            #('name', '=', vals.get('name')),
        ], limit=1, order='name desc')
        print(res_partner_ids)
        return super(PropertyOffer, self).write(vals) """
    
    """ def write(self, vals):
        print(vals)
        res_partner_ids = self.env['res.partner'].browse([10,14])
        print(res_partner_ids.name)
        return super(PropertyOffer, self).write(vals) """
    
    """ def write(self, vals):
        print(self)
        print(self.env.cr)
        print(self.env.uid)
        print(self.env.context)
        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
            #('name', '=', vals.get('name')),
        ]).filtered(lambda x: x.phone == '(870)-931-0505') #mapped('phone')
        print(res_partner_ids)
        return super(PropertyOffer, self).write(vals)
     """
    
