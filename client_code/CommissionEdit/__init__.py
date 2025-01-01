from ._anvil_designer import CommissionEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CommissionEdit(CommissionEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.commission_pending.type = 'number'
    self.commission_received.type = 'number'
    self.due_commission.type = 'number'
    self.status.items = ['Not Paid', 'Fully Paid', 'Partially Paid']

    # Any code you write here will run before the form opens.
