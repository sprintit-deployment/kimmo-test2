# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import api, models, fields

class Module(models.Model):
    _inherit = "ir.module.module"

    def next(self):
        """
        In the context of module packages, we only want to
        refresh the page after module operations without redirects.

        If there is nothing to do this function will try to
        redirect to home after install/upgrade/uninstall.

        We will intercept the redirect and return {'type': 'ir.actions.act_window_close'}
        which will cause _button_immediate_function to return client action 'reload'
        """
        res = super(Module, self).next()
        if not self._context.get('no_redirect'):
            return res

        if res.get('type') == 'ir.actions.act_url' and res.get('url') == '/web':
            return {'type': 'ir.actions.act_window_close'}
        return res

    module_package_ids = fields.Many2many(
        comodel_name="ir.module.package",
        string="Packages",
        readonly=True,
        relation='ir_module_module_ir_module_package_rel',
        column1='ir_module_module_id',
        column2='ir_module_package_id',
    )


    duplicated_source_code = fields.Boolean(
        compute='_compute_duplicated_source_code',
        store=True
    )

    def update_list(self, *args, **kwargs):
        res = super().update_list(*args, **kwargs)
        self.env['ir.module.package'].addon_path_packages()
        return res


    @api.depends('module_package_ids')
    def _compute_duplicated_source_code(self):
        for module in self:
            module.duplicated_source_code = len(module.module_package_ids) > 1

    def _button_immediate_function(self, function):
        """
        In the context of module packages, we only want to
        refresh the page after module operations without redirects.

        Delete params that contains first parent menu id to which redirect
        after install/upgrade/uninstall (usually redirects to Inbox)
        """
        res = super(Module, self)._button_immediate_function(function)
        if not self._context.get('no_redirect'):
            return res

        if 'params' in res:
            del res['params']
        return res
