from odoo import models, fields


class UsersReserv(models.Model):
    # _name = 'openacademy.partner'
    _inherit = 'res.users'

    is_reserved = fields.Boolean("reserved", default=False)
    # reservation_id = fields.Many2many('gestiondesreclamtion.reservation', string="reservation", readonly=True)
    # sale_order_line = fields.Many2many('sale.order.line')
    #sale_order = fields.Many2one('sale.order', ondelete='set null', string="devis", index=True)


