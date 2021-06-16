# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2019 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import models, fields, api
import re
import logging

_logger = logging.getLogger(__name__)


RE_IDENTIFIER = re.compile(r'[^\-a-zA-Z0-9]')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_registry = fields.Char('Business ID', size=64)
    einvoice_address = fields.Char('eInvoice Address', size=20, help='For eInvoice address')
    einvoice_operator_identifier = fields.Char(compute='_compute_einvoice_operator_identifier')
    einvoice_operator = fields.Selection(
        selection=[
            ('003723327487', 'Apix Messaging Oy'),
            ('HELSFIHH', 'Aktia Pankki Oyj'),
            ('BAWCFI22', 'Basware Oyj'),
            ('003703575029', 'CGI Suomi Oy'),
            ('CREDIFLOW', 'Crediflow AB'),
            ('DABAFIHH', 'Danske Bank A/S, Suomen sivuliike'),
            ('HANDFIHH', 'Handelsbanken'),
            ('INEXCHANGE', 'InExchange Factorum AB'),
            ('003708599126', 'Open Text Oy'),
            ('003721291126', 'Maventa'),
            ('003726044706', 'Netbox Finland Oy'),
            ('NDEAFIHH', 'Nordea'),
            ('003722319362', 'Oma säästöpankki Oyj'),
            ('OKOYFIHH', 'OP Osuuskunta'),
            ('E204503', 'OpusCapita Solutions Oy'),
            ('003723609900', 'Pagero Oy'),
            ('POPFFI22', 'POP Pankki'),
            ('003710948874', 'Posti Messaging Oy'),
            ('003701150617', 'PostNord Strålfors Oy'),
            ('003714377140', 'Ropo Capital Oy'),
            ('ITELFIHH', 'Säästöpankit'),
            ('003714756079', 'Telia Finland Oyj'),
            ('003701011385', 'TietoEVRY Oyj'),
            ('003722207029', 'Åland Post Ab'),
            ('AABAFI22', 'Ålandsbanken Abp'),
            # These are not visible on https://verkkolaskuosoite.fi/
            ('EXPSYS', 'Kofax Expert Systems'), # Visible = False
            ('SBANFIHH', 'S-Pankki'), # Visible = False
            ('00885060259470028', 'Tradeshift'), # Visible = False
            ('FIYAPSOL', 'YAP Oy'), # Visible = False
        ],
        string='eInvoice Operator',
        help='For eInvoice operator address',
    )

    @api.depends('einvoice_operator')
    def _compute_einvoice_operator_identifier(self):
        for partner in self:
            partner.einvoice_operator_identifier = partner.einvoice_operator


    def _fix_company_identifers(self, values):
        for field in ['company_registry', 'einvoice_address']:
            if not values.get(field):
                continue
            sanitized = RE_IDENTIFIER.sub('', values[field])
            if values[field] != sanitized:
                _logger.debug("Fixing field '%s' from %s to %s",
                    field, repr(values[field]), repr(sanitized))
                values[field] = sanitized

    @api.model
    def create(self, values):
        self._fix_company_identifers(values)
        return super(ResPartner, self).create(values)

    def write(self, values):
        self._fix_company_identifers(values)
        return super(ResPartner, self).write(values)


    def _commercial_fields(self):
        """ Returns the list of fields that are managed by the commercial entity
        to which a partner belongs. These fields are meant to be hidden on
        partners that aren't `commercial entities` themselves, and will be
        delegated to the parent `commercial entity`. The list is meant to be
        extended by inheriting classes. """
        return super(ResPartner, self)._commercial_fields() + ['company_registry',]


# link partner fields to company as well
class ResCompany(models.Model):
    _inherit = 'res.company'

    company_registry = fields.Char(related='partner_id.company_registry', readonly=False)
    einvoice_address = fields.Char(related='partner_id.einvoice_address', readonly=False)
    einvoice_operator = fields.Selection(related='partner_id.einvoice_operator', readonly=False)
    einvoice_operator_identifier = fields.Char(related='partner_id.einvoice_operator_identifier')
