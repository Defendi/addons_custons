
from odoo import models,fields,api,_


class Project(models.Model):
    _inherit = 'project.project'

    displayed_image_id = fields.Many2one(
        'ir.attachment', 
        domain="[('res_model', '=', 'project.project'), ('res_id', '=', id), ('mimetype', 'ilike', 'image')]", 
        string='Cover Image'
    )
