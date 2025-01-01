from ._anvil_designer import SalesEditTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SalesEdit(SalesEditTemplate):
  def __init__(self, **properties):
    # item = self.item
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.commission.type = 'number'
    self.discount.type = 'number'
    self.order_value.type = 'number'
    # Any code you write here will run before the form opens.



