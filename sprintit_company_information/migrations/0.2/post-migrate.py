
import logging
import re

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

RE_IDENTIFIER = re.compile(r'[^\-a-zA-Z0-9]')

def migrate(cr, version):
    _logger.info("Current version: %s", version)

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        partners = env['res.partner'].search([
            '|',
            ('company_registry', '!=', False),
            ('einvoice_address', '!=', False),
        ])
        for partner in partners:
            for field in ['company_registry', 'einvoice_address']:
                if not partner[field]:
                        continue
                sanitized = RE_IDENTIFIER.sub('', partner[field])
                if partner[field] != sanitized:
                    _logger.debug("Fixing field '%s' from %s to %s", field, repr(partner[field]), repr(sanitized))
                    partner[field] = sanitized
