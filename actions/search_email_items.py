from .lib.base import BaseGraphAction


class SearchItemsAction(BaseGraphAction):
    def run(self, folder_path, subject=None, is_read=False,
            filter_query=None, select_query=None, top=10):

        folder = self.account.root.get_folder_by_name(folder)
        if subject:
            items = folder.filter(subject__contains=subject)
        else:
            items = folder.all()

        return [item_to_dict(item, include_body=include_body) for item in items]
