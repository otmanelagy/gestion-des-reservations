from pprint import pprint

from odoo import models, fields, api


class ReservAssociate(models.Model):
    # _name = 'openacademy.partner'
    _inherit = 'sale.order'
    reservation_ids = fields.One2many('gestiondesreclamtion.reservation', 'devs')

    reservations_count = fields.Integer(compute='_get_reservation_count')

    @api.depends('reservation_ids')
    def _get_reservation_count(self):
        for r in self:
            r.reservations_count = len(r.reservation_ids)
            print(r.reservations_count)

    def reservation_view_invoice(self):
        print("reservation test")

        if self.reservations_count > 1:
            #action['domain'] = [('id', ' in', self.reservation_ids.ids)]
            print("reservation test 111")
            action = {
                "name": "reservation",
                "views": [[False, "tree"], [False, "form"]],
                "view_mode": "tree",
                "res_model": 'gestiondesreclamtion.reservation',
                "view_id": self.env.ref('gestiondesreclamtion.gestiondesreclamtion_tree1').id,
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
                "view_id": self.env.ref('gestiondesreclamtion.gestiondesreclamtion_tree1').id,
                "view_mode": "tree,form",
                "domain": [('id', '=', self.reservation_ids.id)],
                "type": 'ir.actions.act_window'
            }
            # tree_view = [(self.env.ref('gestiondesreclamtion.gestiondesreclamtion_tree1')).id, 'tree']
            # action['views'] = tree_view
            # action['view_mode'] = 'tree'
            # action['res_id'] = self.reservation_ids.id
            # print("reservation test 333")
            # pprint(action)
        return action

