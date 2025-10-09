
from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    document_page_ids = fields.One2many(
        string="Wiki", comodel_name="document.page", inverse_name="task_id"
    )
    document_page_count = fields.Integer(compute="_compute_document_page_count")

    def _compute_document_page_count(self):
        for rec in self:
            rec.document_page_count = len(rec.document_page_ids)

    def action_document_page_tasks(self):
        """Retorna a action equivalente ao record XML `action_document_page_tasks`."""
        # tenta usar o record atual; se for chamado sem record, tenta buscar active_id do contexto
        if self:
            self.ensure_one()
            active_id = self.id
            project_id = self.project_id.id if self.project_id else False
        else:
            active_id = self.env.context.get('active_id')
            if not active_id:
                return {}
            src = self.env['project.task'].browse(active_id)
            project_id = src.project_id.id if src and src.project_id else False

        # referências às views/search (substituir se os XML IDs forem diferentes)
        list_view = self.env.ref('document_page.view_wiki_tree').id
        form_view = self.env.ref('document_page.view_wiki_form').id
        search_view = self.env.ref('document_page.view_wiki_filter').id
        ctx = dict(self.env.context)         # copia o contexto atual
        ctx.update({
            'default_type': 'content',
            'default_project_id': project_id,
            'default_task_id': active_id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task Wiki',
            'res_model': 'document.page',
            'domain': [('type', '=', 'content'), ('task_id', '=', active_id)],
            'context': ctx,
            'view_mode': 'list,form',
            'views': [(list_view, 'list'), (form_view, 'form')],
            'search_view_id': search_view,
            'help': "<p class='oe_view_nocontent_create'>Click to create a new web page.</p>",
            # 'target': 'current' ou 'new' se quiser forçar; XML original não especificava
        }
