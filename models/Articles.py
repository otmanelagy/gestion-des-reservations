from odoo import models, fields

class Article(models.Model):
    _name = 'gestiondesreclamtion.articles'
    name = fields.Char(string="name", required=True)
    description = fields.Text()
    art_resp = fields.Many2one('res.partner', string="responsible", ondelete='set null', index=True)

# class MesReservation(models.Model):