import json
from odoo import http
from odoo.http import request

class DashboardController(http.Controller):
    @http.route('/dashboard/data/', website=True, auth='public') 
    def dashboard_data(self, **kw):
        data = request.env['consolidated.table'].get_dashboard_data()
        print(data)
        return request.make_response(
            json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
    
    @http.route('/dashboard/embed/', type='http', auth='public', website=True)
    def embed_dashboard(self):
        # Enlace oculto
        dashboard_url = "https://app.powerbi.com/viewr=eyJrIjoiN2UyZDUzZTUtMTZmMi00YjMwLWFlZTEtZTk2NzQ1NjJhZ[...]6IjBiMTgwYjAyLTIzMTUtNDBjMS05ZWIxLTY0MDk4N2FmNDRkYyIsImMiOjl9"
        return request.render('student_contract_management.dashboard_embed_template', {'dashboard_url': dashboard_url})