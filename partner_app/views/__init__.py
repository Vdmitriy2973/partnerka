from .dashboard import dashboard
from .index import index
from .logout import logout_view

# Страницы рекламодателя
from .advertiser_views.advertiser_dashboard import advertiser_dashboard
from .advertiser_views.advertiser_partners import advertiser_partners
from .advertiser_views.advertiser_sales import advertiser_sales
from .advertiser_views.advertiser_projects import advertiser_projects
from .advertiser_views.advertiser_requisites import advertiser_requisites
from .advertiser_views.advertiser_settings import advertiser_settings

# Функциии рекламодателя
from .advertiser_views.advertiser_operations.project import add_project, delete_project,edit_project, approve_project, reject_project
from .advertiser_views.advertiser_operations.update_api_settings import update_api_settings
from .advertiser_views.advertiser_operations.top_up_balance import top_up_balance

# Страницы партнёра
from .partner_views.partner_dashboard import partner_dashboard
from .partner_views.partner_offers import partner_offers
from .partner_views.partner_connections import partner_connections
from .partner_views.partner_platforms import partner_platforms
from .partner_views.partner_links import partner_links
from .partner_views.partner_payments import partner_payments
from .partner_views.partner_settings import partner_settings

# Функции партнёра
from .partner_views.partner_operations.connect_project import connect_project
from .partner_views.partner_operations.generate_partner_link import generate_link
from .partner_views.partner_operations.delete_partner_link import delete_partner_link
from .partner_views.partner_operations.update_partner_payout_settings import payout_settings_view


from .platform import add_platform, delete_platform, approve_platform,reject_platform, edit_platform


from .process_adv_transaction import proccess_adv_transaction, approve_adv_transaction, reject_adv_transaction


from .advertiser_views.advertiser_operations.update_requisites import update_requisites_settings

from .update_notifications import update_notifications_settings

# Страницы с инфомацией о сущностях
from .user_views.partner_detail import partner_detail
from .user_views.advertiser_detail import advertiser_detail
from .user_views.advertiser_legal_details import advertiser_legal_details
from .user_views.project_detail import project_detail

from .partnership import stop_partnership_with_project,stop_partnership_with_partner, suspend_partnership, resume_partnership



from .api_documetation import api_docs

# REST API
from .api.api_protected import ProtectedAPIView
from .api.api_conversion import ConversionAPIView
from .api.api_click import ClickAPIView


from .transactions import create_payout_request, approve_transaction, reject_transaction

from .block_user import block_user
from .unblock_user import unblock_user