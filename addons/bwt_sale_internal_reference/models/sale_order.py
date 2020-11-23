# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_ref = fields.Char(string='Internal Reference', readonly=True)

    user_id = fields.Many2one('res.users', string='User')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.internal_ref = "Hello " + self.user_id.name