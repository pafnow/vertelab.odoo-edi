# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    route_id = fields.Many2one(comodel_name="edi.route")
    
    @api.one
    def _message_count(self):
        self.message_count = self.env['edi.message'].search_count([('model','=',self._name),('res_id','=',self.id)])
    message_count = fields.Integer(compute='_message_count',string="# messages")
    

    @api.model
    def create(self, vals):
        order =  super(sale_order,self).create(vals)
        if order:
            order.route_id.edi_action('sale.order.create',order=order)
        return order
    @api.model
    def action_cancel(self):
        res =  super(sale_order,self).action_cancel()        
        self.route_id.edi_action('sale.order.action_cancel',order=self[0],res=res)
        return res
    @api.model
    def action_button_confirm(self):
        return super(sale_order,s).action_button_confirm() 
        for s in self:
            res =  super(sale_order,s).action_button_confirm()        
            if s.route_id:
                s.route_id.edi_action('sale.order.action_button_confirm',order=s,res=res)
        return res
    @api.model
    def action_wait(self):
        res =  super(sale_order,self).action_wait()        
        self.route_id.edi_action('sale.order.action_wait',order=self[0],res=res)
        return res
    @api.model
    def action_done(self):
        res =  super(sale_order,self).action_done()        
        self.route_id.edi_action('sale.order.action_done',order=self[0],res=res)
        return res
    @api.model
    def action_ship_create(self):
        res =  super(sale_order,self).action_ship_create()        
        self.route_id.edi_action('sale.order.action_ship_create',order=self[0],res=res)
        return res
    @api.model
    def action_invoice_create(self, grouped=False, states=None, date_invoice = False):
        res =  super(sale_order,self).action_invoice_create(grouped=grouped, states=states, date_invoice = date_invoice)        
        invoices = [i for i in self[0].invoice_ids if i.state == 'draft']
        if len(invoices)>0:
            self.route_id.edi_action('sale.order.action_invoice_create',order=self[0],invoice=invoices[-1])
        return res
    @api.model
    def action_invoice_cancel(self):
        res =  super(sale_order,self).action_invoice_cancel()        
        self.route_id.edi_action('sale.order.action_invoice_cancel',order=self[0],res=res)
        return res
    @api.model
    def action_invoice_end(self):
        res =  super(sale_order,self).action_invoice_end()        
        self.route_id.edi_action('sale.order.action_invoice_end',order=self[0],res=res)
        return res    
    @api.model
    def action_ignore_delivery_exception(self):
        res =  super(sale_order,self).action_ignore_delivery_exception()        
        self.route_id.edi_action('sale.order.action_ignore_delivery_exception',order=self[0],res=res)
        return res
     
    def _edi_message_create(self, edi_type):
        self.env['edi.message']._edi_message_create(edi_type=edi_type, obj=self, partner=self.partner_id, check_route=False, check_double=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: