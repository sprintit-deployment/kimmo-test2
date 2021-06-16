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

from odoo.modules.graph import Node, Graph

_logger = logging.getLogger(__name__)
GRAPH_CACHE = {}


class SpecialGraph(Graph):

    def add_node(self, name, info):
        """We want to overwrite this to add child to every father that was found,
        not just to the father that has the highest depth. This way we get a nicer print out"""
        added = None
        for d in info['depends']:
            father = self.get(d)
            added = father.add_child(name, info)
        if added:
            return added
        else:
            return Node(name, self, info)
    

def create_graph(cr):
    """All these definitions and imports are only needed for our one shared graph instance,
    Which means we only need them in this local scope
    """
    
    graph = SpecialGraph()
    cr.execute("SELECT name FROM ir_module_module")
    modules = [r['name'] for r in cr.dictfetchall()]
    _logger.warning("Loading all available modules in to a dependency graph instance")
    graph.add_modules(cr, modules)
    return graph


def get_graph(cr):
    """To avoid loading modules multiple times we cache our graph instance,
    and use it for computing the dependency graph for every module package"""

    if 'graph' not in GRAPH_CACHE:
        GRAPH_CACHE['graph'] = create_graph(cr)

    return GRAPH_CACHE['graph']


def node_pprint(self, depth=0):
    "Add depth to the original _pprint() from odoo.modules.graph.Node class"
    s = '%s\n' % (self.name,)
    for c in self.children:
        s += '%s`-> (%s) %s' % ('   ' * depth, c.depth, node_pprint(c, depth+1))
    return s
