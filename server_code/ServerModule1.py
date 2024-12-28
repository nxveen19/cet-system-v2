import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_movie(customer_data):
  if movie_data.get('direct') and movie_data.get('movie_name') and movie_data.get('summary') and movie_data.get('year'):
      app_tables.movies.add_row(**movie_data)n 42
#
