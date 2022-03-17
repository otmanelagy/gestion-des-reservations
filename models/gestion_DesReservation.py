# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError

from .res_users import UsersReserv


class Resevation(models.Model):
    _name = 'gestiondesreclamtion.reservation'
    # name = fields.Char(string="Title", required=True)
    reservation_ref = fields.Char(string='RESERVE', readonly=True,
                                  copy=False)
    client_id = fields.Many2one('res.users',
                                ondelete='cascade', string="client", index=True)
    articles_id = fields.Many2one('gestiondesreclamtion.articles',
                                  ondelete='set null', string="articles", index=True)
    reservation_date = fields.Date(default=datetime.date.today())
    month = fields.Integer('month', default='0')
    days = fields.Integer('days', default='0')
    hours = fields.Integer('hours', default='0')
    color = fields.Integer()
    # operator_id = fields.Many2one('res.users', 'Operator', default=lambda self: self.env.user, readonly=True)

    devs = fields.Many2one('sale.order', ondelete='set null', string="devis", index=True)
    # devs_associate = fields.Many2one('sale.order', ondelete='set null', string="devis", index=True)
    reservation_end_date = fields.Date(string="End Date", store=True, compute='_get_end_date')

    hours_ex = fields.Integer(string="hours number", store=True, compute='_get_hours')

    month_ex = fields.Integer(string="End Date", store=True, compute='_get_month')

    @api.depends('month', 'days', 'hours')
    def _get_hours(self):
        for r in self:
            r.hours_ex = (r.month*30 + r.days)*24 + r.hours

    @api.depends('reservation_date')
    def _get_month(self):
        print('====> ')
        for r in self:
            start_date = fields.Datetime.from_string(r.reservation_date)
            r.month_ex = start_date.month

    state = fields.Selection([
        ('nouvelle', "Nouvelle"),
        ('confirmed', "Confirmed"),
        ('valid', "Valid"),
        ('annulled', "Annulled"),
        ], default='nouvelle')

    reservation_count = fields.Integer(
        string="Attendees count", compute='_get_reserv_count', store=True)

    @api.depends('reservation_ref')
    def _get_reserv_count(self):
        for r in self:
            r.reservation_count = len(r.reservation_ref)

    def create_quotation(self):
        duration = (self.month * 30 + self.days) * 24 + self.hours
        price = 0
        order = self.env['sale.order'].search([], limit=1)
        if duration < 10:
            price = 150.00
        else:
            price = 140.00
            # if self.state == 'valid':
        # devs = self.env['sale.order'].sudo()
        sale_order_cost = self.devs.create({
            'date_order': self.reservation_date,
            'name': self.reservation_ref,
            'order_line': [
                (0, 0, {
                    'price_unit': price,
                    'product_uom_qty': duration,
                    'product_id': self.articles_id.id})],
            'partner_id': self.client_id.partner_id.id,
            'pricelist_id': order.pricelist_id.id,
        })
        self.devs = sale_order_cost
        # else: self    for record in self
        #     raise ValidationError("vous pouvez pas creer un devis pour une reservation non validee")

    def many_quotation(self):
        price = 0
        # order = self.env['sale.order'].search([], limit=1)
        users = set(self.client_id)
        print("====>", users)
        ER = False
        for user in users:
            reserve = [record for record in self if record.client_id == user]
            sale_order_cost = self.env['sale.order'].create({
                # 'name': reserve.reservation_ref,
                'partner_id': user.partner_id.id,
                # 'pricelist_id': order.pricelist_id.id,
            })
            print("====>", reserve)

            for res in reserve:
                if res.state == 'valid':
                    duration = (res.month * 30 + res.days) * 24 + res.hours

                    if duration < 10:
                        price = 150.00
                    else:
                        price = 140.00

                    sale_order_cost.order_line = [(0, 0, {
                        'name': res.reservation_ref,
                        'price_unit': price,
                        'product_uom_qty': duration,
                        'product_id': res.articles_id.id
                    })]
                else:
                    ER = True
            res.devs = sale_order_cost
        if ER:
            raise ValidationError("vous pouvez pas creer un devis pour une reservation non valide")

    def action_nouvelle(self):
        self.state = 'confirmed'

    def action_confirmed(self):
        self.state = 'valid'

    def action_valid(self):
        self.state = 'annulled'

    def action_annulled(self):
        self.state = 'nouvelle'

    @api.depends('reservation_date', 'month', 'days', 'hours')
    def _get_end_date(self):
        for r in self:
            duration = datetime.timedelta(days=r.days + (r.month * 30), hours=r.hours)
            if not (r.reservation_date and duration):
                r.reservation_end_date = r.reservation_date
                continue
            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start_date = fields.Datetime.from_string(r.reservation_date)
            r.reservation_end_date = start_date + duration

    # def _set_end_date(self):
    #     for r in self:
    #         if not (r.reservation_date and r.reservation_end_date):
    #             continue
    #
    #         reservation_date = fields.Datetime.from_string(r.reservation_date)
    #         end_date = fields.Datetime.from_string(r.reservation_end_date)
    #         r.duration = (end_date - reservation_date).days + 1

    @api.constrains('days', 'hours')
    def _check_instructor(self):
        for records in self:
            if records.days > 30 or records.days < 0:
                raise ValidationError("days shouldn't be negative or more than 30d")
            if records.hours > 24:
                raise ValidationError("hours shouldn't be negative or more than 24h ")

    @api.model
    def create(self, vals):
        print('====> before', vals.get('reservation_ref'))
        if not vals.get('reservation_ref'):
            print('===> before', self.client_id.reserved)
            vals['reservation_ref'] = self.env['ir.sequence'].next_by_code('gestion.reclamation')

        res = super(Resevation, self).create(vals)
        reserved = res.client_id.reserved
        print('==> after', reserved)
        res.client_id.reserved = True
        return res

    def unlink(self):
        # values['client_id.reserved'] = False
        for r in self:
            r.client_id.reserved = False
        res = super(Resevation, self).unlink()

        return res



