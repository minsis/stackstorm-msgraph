# Microsoft Graph API Integration Pack

This pack gives integration into [Microsoft's Graph API v1.0](https://docs.microsoft.com/en-us/graph/)

## Documentation

A list of some useful reference documentation for interacting with Graph

* [OData Query Parameters and Usage](https://docs.microsoft.com/en-us/graph/query-parameters) 

## Actions
Note that most actions will allow you to specify a custom OData query and select statements.
These actions also include a simplified quick access to some common OData parameters.
If the `filter_query` is specified the common parameters will be ignored and the custom query will be used.
The data returned from the action will vary but  will all be in the json output that comes from the Graph API.
The  keys will be converted to lower-case, but the rest stays the same.

### * `search_mail_items` 
Searches email items in a given folder.

Parameters Include:
* `account` Specify the account name that is defined in the pack's config file.
* `folder_path` The mail folder path in a unix-like format. e.g. `Inbox/MyCoolFolder/ReallyAwesomeEmails`
* `subject` The subject to search for. This is a contains function and not an exact match.
* `is_read` Flag for searching messages are read or not. By default all mail items are returned.
* `select_query` The OData select query
* `filter_query` The OData filter query
* `top` Get the top n items. Defaults to 10
