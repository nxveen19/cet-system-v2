from ._anvil_designer import OrdersEditTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OrdersEdit(OrdersEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.status.items = ['Order Placed', 'Deposit Received', 'Installed']
    self.installation_status.items = []

    # Any code you write here will run before the form opens.
