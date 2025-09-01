from .dashboard import dashboard
from .index import index
from .logout import logout_view


from .advertiser_views.dashboard import advertiser_dashboard
from .advertiser_views.partners import advertiser_partners
from .advertiser_views.sales import advertiser_sales
from .advertiser_views.projects import advertiser_projects
from .advertiser_views.requisites import advertiser_requisites
from .advertiser_views.settings import advertiser_settings

from .platform import add_platform, delete_platform, approve_platform,reject_platform, edit_platform
from .project import add_project, delete_project, approve_project, reject_project,edit_project
from .connect_project import connect_project
from .top_up_balance import top_up_balance
from .process_adv_transaction import proccess_adv_transaction, approve_adv_transaction, reject_adv_transaction

from .update_api_settings import update_api_settings
from .update_requisites import update_requisites_settings

from .update_notifications import update_notifications_settings

from .partner_detail import partner_detail
from .advertiser_detail import advertiser_detail
from .advertiser_requisites import advertiser_requisites

from .partnership import stop_partnership_with_project,stop_partnership_with_partner, suspend_partnership, resume_partnership
from .project_detail import project_detail
from .generate_partner_link import generate_link
from .delete_partner_link import delete_partner_link

from .api_documetation import api_docs

# REST API
from .api.api_protected import ProtectedAPIView
from .api.api_conversion import ConversionAPIView
from .api.api_click import ClickAPIView

from .update_partner_payout_settings import payout_settings_view
from .transactions import create_payout_request, approve_transaction, reject_transaction

from .block_user import block_user
from .unblock_user import unblock_user