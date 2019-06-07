

class DBRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'export':
            return 'rails-db'
        return None
