# user

Manage a Linode User.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a basic user
  linode.cloud.user:
    username: my-cool-user
    email: user@linode.com
    restricted: false
    state: present
```

```yaml
- name: Create a user that can only access Linodes
  linode.cloud.user:
    username: my-cool-user
    email: user@linode.com
    grants:
      global:
        add_linodes: true
      resources:
        - type: linode
          id: 12345
          permissions: read_write
    state: present
```

```yaml
- name: Delete a user
  linode.cloud.user:
    username: my-cool-user
    state: absent
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | `str` | **Required** | The username of this user.   |
| `state` | `str` | **Required** | The state of this user.  (Choices:  `present`  `absent` ) |
| `restricted` | `bool` | Optional | If true, the User must be granted access to perform actions or access entities on this Account.  (Default: `True`) |
| `email` | `str` | Optional | The email address for the User. Linode sends emails to this address for account management communications. May be used for other communications as configured.   |
| [`grants` (sub-options)](#grants) | `dict` | Optional | Update the grants a User has.   |





### grants

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`global` (sub-options)](#global) | `dict` | Optional | A structure containing the Account-level grants a User has.   |
| [`resources` (sub-options)](#resources) | `list` | Optional | A list of resource grants to give to the user.   |





### global

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `account_access` |  | Optional | The level of access this User has to Account-level actions, like billing information. A restricted User will never be able to manage users.  (Choices:  `read_only`  `read_write` ) |
| `add_databases` | `bool` | Optional | If true, this User may add Managed Databases.  (Default: `False`) |
| `add_domains` | `bool` | Optional | If true, this User may add Domains.  (Default: `False`) |
| `add_firewalls` | `bool` | Optional | If true, this User may add firewalls.  (Default: `False`) |
| `add_images` | `bool` | Optional | If true, this User may add images.  (Default: `False`) |
| `add_linodes` | `bool` | Optional | If true, this User may add Linodes.  (Default: `False`) |
| `add_longview` | `bool` | Optional | If true, this User may add LongView.  (Default: `False`) |
| `add_nodebalancers` | `bool` | Optional | If true, this User may add NodeBalancers.  (Default: `False`) |
| `add_stackscripts` | `bool` | Optional | If true, this User may add StackScripts.  (Default: `False`) |
| `add_volumes` | `bool` | Optional | If true, this User may add volumes.  (Default: `False`) |
| `cancel_account` | `bool` | Optional | If true, this User may add cancel the entire account.  (Default: `False`) |
| `longview_subscription` | `bool` | Optional | If true, this User may manage the Account’s Longview subscription.  (Default: `False`) |





### resources

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `type` |  | **Required** | The type of resource to grant access to.  (Choices:  `domain`  `image`  `linode`  `longview`  `nodebalancer`  `stackscript`  `volume` ) |
| `id` | `int` | **Required** | The ID of the resource to grant access to.   |
| `permissions` | `str` | **Required** | The level of access this User has to this entity. If null, this User has no access.  (Choices:  `read_only`  `read_write` ) |






## Return Values

- `user` - The user in JSON serialized form.

    - Sample Response:
        ```json
        {
          "email": "example_user@linode.com",
          "restricted": true,
          "ssh_keys": [
            "home-pc",
            "laptop"
          ],
          "tfa_enabled": null,
          "username": "example_user"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/account/#user-view__response-samples) for a list of returned fields


- `grants` - The grants info in JSON serialized form.

    - Sample Response:
        ```json
        {
          "domain": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "global": {
            "account_access": "read_only",
            "add_databases": true,
            "add_domains": true,
            "add_firewalls": true,
            "add_images": true,
            "add_linodes": true,
            "add_longview": true,
            "add_nodebalancers": true,
            "add_stackscripts": true,
            "add_volumes": true,
            "cancel_account": false,
            "longview_subscription": true
          },
          "image": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "linode": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "longview": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "nodebalancer": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "stackscript": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ],
          "volume": [
            {
              "id": 123,
              "label": "example-entity",
              "permissions": "read_only"
            }
          ]
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/account/#users-grants-view__response-samples) for a list of returned fields


