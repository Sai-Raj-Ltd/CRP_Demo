# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sairaj_inventory(models.Model):
    _inherit = 'stock.inventory'
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'),('cancel', 'Cancelled'),('cancel', 'Cancelled'),('confirm', 'In Progress'),('approval', 'To Approve'),('done', 'Validated')],copy=False, index=True, readonly=True,default='draft')

    def action_for_approval(self):
        self.state='approval'


class SairajInventoryStockPicking(models.Model):
    _inherit = 'stock.picking'
    state = fields.Selection([('draft', 'Draft'),('waiting', 'Waiting Another Operation'),('confirmed', 'Waiting'),('assigned', 'Ready'),('approval', 'To Approve'),('done', 'Done'),('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
             " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
             " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
             " * Done: has been processed, can't be modified or cancelled anymore.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore.")

    @api.depends('move_type', 'move_lines.state', 'move_lines.picking_id')
    @api.one
    def _compute_state(self):
        # import pdb
        # pdb.set_trace()
        ''' State of a picking depends on the state of its related stock.move
        - Draft: only used for "planned pickings"
        - Waiting: if the picking is not ready to be sent so if
          - (a) no quantity could be reserved at all or if
          - (b) some quantities could be reserved and the shipping policy is "deliver all at once"
        - Waiting another move: if the picking is waiting for another move
        - Ready: if the picking is ready to be sent so if:
          - (a) all quantities are reserved or if
          - (b) some quantities could be reserved and the shipping policy is "as soon as possible"
        - Done: if the picking is done.
        - Cancelled: if the picking is cancelled
        '''

        for i in self:
            if not i.move_lines:
                i.state = 'draft'
            elif any(move.state == 'draft' for move in i.move_lines):  # TDE FIXME: should be all ?
                i.state = 'draft'
            elif all(move.state == 'cancel' for move in i.move_lines):
                i.state = 'cancel'
            elif all(move.state in ['cancel', 'done'] for move in i.move_lines):
                    if (i.picking_type_id.name == 'Delivery Orders') or (i.move_lines.location_id.name=='Input' and i.origin[0:2]=='PO'):
                        i.state = 'approval'
                    else:
                        i.state = 'done'
            else:
                relevant_move_state = i.move_lines._get_relevant_state_among_moves()
                if relevant_move_state == 'partially_available':
                    i.state = 'assigned'
                else:
                    i.state = relevant_move_state


    def action_for_approval_pick(self):
        self.state='done'



