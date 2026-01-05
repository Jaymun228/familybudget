from telegram.ext import Application

from .add_expense import register_add_expense_handlers
from .dashboard import register_dashboard_handlers
from .export import register_export_handlers
from .import_handlers import register_import_handlers
from .menu import register_menu_handlers
from .reports import register_report_handlers


def register_handlers(app: Application) -> None:
    register_menu_handlers(app)
    register_add_expense_handlers(app)
    register_dashboard_handlers(app)
    register_report_handlers(app)
    register_export_handlers(app)
    register_import_handlers(app)
