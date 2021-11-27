from .lib.base import BaseOutlookAction
from .lib.utilities import FilterQueryBuilder


class SearchItemsAction(BaseOutlookAction):
    def run(self, account=None, folder_path="Inbox", subject=None, is_read=None,
            select_query=None, filter_query=None, top=10):

        if account:
            self.account = self.get_account(account)

        folder = self.get_outlook_folder(folder_path)

        if filter_query:
            filters = FilterQueryBuilder(filter_query)
        else:
            filters = FilterQueryBuilder()

            if subject is not None:
                filters.contains("Subject", subject)

            if is_read is not None:
                filters.eq_("isRead", "true")

        messages = folder.messages

        if filters:
            messages = messages.filter(filters())

        if select_query:
            messages = messages.select(select_query)

        items = messages.top(top).get().execute_query()

        return [{k.lower(): v} for item in items for k, v in item.to_json().items()]
