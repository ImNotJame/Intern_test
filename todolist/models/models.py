from odoo import models, fields , api

## Tags
class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")


## LineList
class TodoListLine(models.Model):
    _name = 'todo.listline'
    _description = 'Todo List Line'

    name = fields.Char(string="Sub List", required=True)
    description = fields.Text(string="Description")
    is_done = fields.Boolean(string="Done", default=False)
    list_id = fields.Many2one('todo.list', string="List",required=True,ondelete='cascade')


## Main List
class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="End Date",required=True)

    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking = True
    )

    line_ids = fields.One2many('todo.listline', 'list_id', string="Sub Lists")


    def action_start(self):
        for record in self:
            record.status = 'in_progress'

    def action_complete(self):
        for record in self:
            record.status = 'done'    


    tag_ids = fields.Many2many('todo.tag', string='Tags')

    ## make end date greater than start date Trigger in UI
    @api.onchange('start_date', 'end_date')
    def _onchange_date(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                self.end_date = self.start_date
                
                

    all_lines_done = fields.Boolean(string="All Lines Done", compute="_compute_all_lines_done",store = True)

    ## check if all lines are done Trigger when value is changed
    @api.depends('line_ids.is_done','line_ids')
    def _compute_all_lines_done(self):
        for record in self:
            record.all_lines_done = all(line.is_done for line in record.line_ids) and bool(record.line_ids)



    attendee_ids = fields.Many2many(
        'res.partner',
        string='Attendees',
        tracking=True
    )
                