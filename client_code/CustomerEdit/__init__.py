from ._anvil_designer import CustomerEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CustomerEdit(CustomerEditTemplate):
 def __init__(self, item, **properties):
        # Set the item property
   # self.item here =  elements from item = {} one by one
  self.item = item
  self.init_components(**properties)
  self.init_components(**properties)
  self.phone.type = "number"

    # Any code you write here will run before the form opens.
