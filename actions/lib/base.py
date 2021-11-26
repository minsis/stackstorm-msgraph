import msal

from office365.graph_client import GraphClient
from st2common.runners.base_action import Action


class BaseGraphAction(Action):

    def get_account(self, account="default"):
        """
        Get the user Graph user account

        Since there are two different methods for Graph accounts (signed-in user or retrieve user account)
        the attempt here is make that transparent to any objects making calls

        :param account: The account name as defined in the pack config under 'accounts'
        :type account: string, defaults to "default"
        :return: The Graph user account
        :rtype: :class:`office365`
        """
        try:
            account = self.config.get("accounts")[account]
        except KeyError:
            raise ValueError("The account '{}' is not defined in the config")

        self.client = GraphClient(self._acquire_token)

        self.tenant_id_or_name = account["tenant_id_or_name"]
        self.client_id = account["client_id"]
        self.client_secret = account["client_secret"]
        self.user_principal_name = account.get("user_principal_name")
        self.authority_url = account.get(
            "authority_url",
            "https://login.microsoftonline.com/{}".format(account["tenant_id_or_name"]),
        )
        self.scopes = account.get("scopes") or ["https://graph.microsoft.com/.default"]

        if self.user_principal_name:
            return self.client.users[self.user_principal_name].get().execute_query()
        else:
            return self.client.me.get().execute_query()

    def _acquire_token(self):
        """
        Acquire token via MSAL
        """

        app = msal.ConfidentialClientApplication(
            authority=self.authority_url,
            client_id=self.client_id,
            client_credential=self.client_secret
        )
        token = app.acquire_token_for_client(scopes=self.scopes)
        return token


class BaseOutlookAction(BaseGraphAction):

    def __init__(self):
        super(BaseOutlookAction, self).__init__()

    def _get_outlook_folder(self, folder_path:str):
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
                raise ValueError("Mailbox folder path {} does not seem to exist".format(folder_path))

        return parent
