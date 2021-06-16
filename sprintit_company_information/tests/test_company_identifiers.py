
import logging
import requests


from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)



class CompanyIdentifierTest(TransactionCase):

    def test_einvoice_operator(self):
        # This API endpoint was fould by inspecting https://verkkolaskuosoite.fi/ network calls so it isn't quaranteed to stay.
        res = requests.put('https://verkkolaskuosoite.fi/server/Owner/list', headers={'Content-Type': 'application/json'}, json={"countryCode":"FI"})
        operators_list = res.json()
        selection_dict = dict(self.env['res.partner']._fields['einvoice_operator'].selection)
        for operator in operators_list:
            if operator['visible']:
                self.assertEqual(selection_dict.get(operator['serviceId'][0], 'Missing!'), operator['name'].strip(), msg="Incorrect eInvoice Operator. Did they change their company name?")



    def test_company_identifiers(self):
        partner = self.env.company.partner_id
        inputs = {
            '203\xa032': '20332',
            '\n20332\n': '20332',
            '\t20332\t': '20332',
            ' \t2033-2\t ': '2033-2',
            '003714600541': '003714600541',
            'FI0540550010273734': 'FI0540550010273734',
            '0626103-3': '0626103-3',
        }

        for input_str, expected in inputs.items():
            for field in ['company_registry', 'einvoice_address']:
                partner[field] = input_str
                self.assertEqual(partner[field], expected, msg="Company idenfier %s was not sanitized correctly: %s != %s" % (field, repr(partner[field]), repr(expected)))



