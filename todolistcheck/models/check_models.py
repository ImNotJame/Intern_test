from custom_addons.todolistcheck.models.check_models import models,fields

class TodoCheck(models.Model):
    _name = 'todo.check'
    _description = 'Todo Check'

    name = fields.Char(string="Check Name", required=True)
    todolist_id = fields.Char(string="Check name",required=True)