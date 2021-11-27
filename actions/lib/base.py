from msal import ConfidentialClientApplication
from office365.graph_client import GraphClient
from st2common.runners.base_action import Action

from .decorators import requires_account


class BaseGraphAction(Action):
    def __init__(self, config):
        super().__init__(config)

        self.account = None

    def get_account(self, account="default"):
        """
        Get the user Graph user account

        Since there are two different methods for Graph accounts (signed-in user or retrieve user account)
        the attempt here is make that transparent to any objects making calls

        :param account: The account name as defined in the pack config under 'accounts'
        :type account: string, defaults to "default"
        :return: The Graph user account object
        :rtype: :class:`office365.runtime.client_path.ClientPath`
        """
        try:
            account = self.config.get("accounts")[account]
        except KeyError:
            raise ValueError("The account '{}' is not defined in the config".format(account))

        client_id = account["client_id"]
        client_secret = account["client_secret"]
        user_principal_name = account.get("user_principal_name")
        authority_url = account.get(
            "authority_url",
            "https://login.microsoftonline.com/{}".format(account["tenant_id_or_name"]),
        )
        scopes = account.get("scopes", ["https://graph.microsoft.com/.default"])

        def _acquire_token():
            app = ConfidentialClientApplication(
                authority=authority_url,
                client_id=client_id,
                client_credential=client_secret
            )
            token = app.acquire_token_for_client(scopes=scopes)
            return token

        client = GraphClient(_acquire_token)

        if user_principal_name:
            return client.users[user_principal_name].get().execute_query()
        else:
            return self.client.me.get().execute_query()


class BaseOutlookAction(BaseGraphAction):

    @requires_account
    def get_outlook_folder(self, folder_path: str):
        """
        Search for a folder within outlook

        :param folder_path: The mailbox folder path you want to return as a unix path-like format
            For example 'Inbox/MyCoolFolder/ReallyAwesomeEmails'
            Case insensitive
        :type folder_path: string, required
        :return: Returns a MailFolder object
        :rtype: :class:`office365.outlook.mail.mail_folder.MailFolder`
        """

        if folder_path.startswith("/"):
            folder_path = folder_path[1:]

        if folder_path.endswith("/"):
            folder_path = folder_path[:-1]

        parent = None
        for folder in folder_path.strip().split("/"):
            try:
                if not parent:
                    parent = self.account.mail_folders.filter(
                        "displayName eq {}".format(folder)
                    ).get().execute_query()[0]
                else:
                    parent = parent.child_folders.filter(
                        "displayName eq {}".format(folder)
                    ).get().execute_query()[0]
            except IndexError:
                raise ValueError("Mailbox folder path '{}' does not seem to exist".format(folder_path))

        return parent
