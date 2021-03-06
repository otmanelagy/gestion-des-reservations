from pprint import pprint

from odoo import models, fields, api


class ReservAssociate(models.Model):

    _inherit = 'sale.order'

    reservation_ids = fields.One2many('gestiondesreclamtion.reservation', 'sale_order')

    reservations_count = fields.Integer(compute='_get_reservation_count')

    @api.depends('reservation_ids')
    def _get_reservation_count(self):
        # count the total of reservation related to on quotation
        for r in self:
            r.reservations_count = len(r.reservation_ids)
            print(r.reservations_count)

    def reservation_view_invoice(self):
        # action of smart button : display reservations
        print("reservation test")
        if self.reservations_count > 1:
            # action['domain'] = [('id', ' in', self.reservation_ids.ids)]
            print("reservation test 111")
            action = {
                "name": "reservation",
                "views": [[False, "tree"], [False, "form"]],
                "view_mode": "tree",
                "res_model": 'gestiondesreclamtion.reservation',
                "view_id": self.env.ref('gestiondesreclamtion.gestiondesreclamtion_tree1_view').id,
                "view_mode": "tree,form",
                "domain": [('id', ' in ', self.reservation_ids.ids)],
                "type": 'ir.actions.act_window'
            }
        elif self.reservation_ids:
            print("reservation test 222")
            action = {
                "name": "reservation",
                "views": [[False, "tree"], [False, "form"]],
                "view_mode": "tree",
                "res_model": 'gestiondesreclamtion.reservation',
                "view_id": self.env.ref('gestiondesreclamtion.gestiondesreclamtion_tree1_view').id,
                "view_mode": "tree,form",
                "domain": [('id', '=', self.reservation_ids.id)],
                "type": 'ir.actions.act_window'
            }

        return action
