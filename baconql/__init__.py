import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
