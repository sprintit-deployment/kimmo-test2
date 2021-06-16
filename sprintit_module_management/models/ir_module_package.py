# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

import logging
import glob
import os

from odoo import models, fields, api
from odoo.tools.config import config

from ..helpers import get_graph, node_pprint

log = logging.getLogger(__name__)


class IrModulePackage(models.Model):
    _name = "ir.module.package"
    _description = 'Module Package'
    _inherit = ['mail.thread']
    _order = 'sequence asc, id'

    sequence = fields.Integer()

    name = fields.Char(required=True)

    module_ids = fields.Many2many(
        comodel_name="ir.module.module",
        string="Modules",
        readonly=False,
        relation='ir_module_module_ir_module_package_rel',
        column1='ir_module_package_id',
        column2='ir_module_module_id',
    )

    dependency_graph = fields.Html(
        string='Dependency HTML',
        sanitize=False,
        compute="_compute_dependency_graph",
        # This is only for developing/debugging, no need to compute otherwise
        groups='base.group_no_one',
    )

    auto_generated = fields.Boolean(help="Technical field to help deletion of old addon path based packages")

    _sql_constraints = [(
        'name_unique',
        'unique(name)',
        'Database already has a package with this name!'
    )]

    def addon_path_packages(self):
        folders = config['addons_path'].split(',')
        updated_packages = self.env['ir.module.package']
        for i, folder in enumerate(folders, start=1):
            if not os.path.isdir(folder):
                continue
            glob_path = os.path.join(folder, '*')
            names = [os.path.basename(p) for p in glob.glob(glob_path)]
            modules = self.env['ir.module.module'].search([('name', 'in', names)])
            if not modules:
                continue
            package = self.search([('name', '=', folder)])
            if not package:
                package = self.create({'name': folder})

            package.auto_generated = True
            package.module_ids = modules
            package.sequence = i

            updated_packages += package

        addon_path_removed = self.search([
            ('auto_generated', '=', True),
            ('id', 'not in', updated_packages.ids)
        ])
        addon_path_removed.unlink()



    def button_immediate_upgrade(self):
        self.ensure_one()
        return self.module_ids.filtered(lambda x: x.state == 'installed').button_immediate_upgrade()

    def hard_reset_apps_list(self):
        """Run this if module folders have been removed from the server."""
        self.env['ir.module.module'].search([('state', '=', 'uninstalled')]).unlink()
        return self.reset_apps_list()


    def reset_apps_list(self):
        self.env['ir.module.module'].update_list()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _compute_dependency_graph(self):
        for record in self:
            graph = get_graph(record.env.cr)
            modules = record.module_ids.filtered(lambda x: x.name in graph).sorted(lambda x: len(graph[x.name].children), reverse=True)
            message = []
            printed = set()
            for module in modules:
                if module.name not in printed:
                    node = graph[module.name]
                    printed.add(node.name)
                    printed.update([n.name for n in node.children])
                    parents = set(node.parents)
                    message.append("Parents ({}):".format(', '.join([p.name for p in parents])))
                    message.append(node_pprint(node))

            message_str = '\n'.join(message)
            record.dependency_graph = "<pre>{}</pre>".format(message_str)


    def button_immediate_install(self):
        self.ensure_one()
        not_installed = self.module_ids.filtered(lambda x: x.state != 'installed')
        all_dependencies_available = not_installed.filtered(lambda x: 'unknown' not in x.mapped('dependencies_id.state'))
        return all_dependencies_available.button_immediate_install()
