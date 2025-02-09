"""This module contains the base Linode module that other modules inherit from."""

from __future__ import absolute_import, division, print_function

import traceback
from typing import Any

try:
    from ansible.module_utils.ansible_release import __version__ as ANSIBLE_VERSION
except Exception:
    ANSIBLE_VERSION = 'unknown'

from ansible.module_utils.basic import AnsibleModule, missing_required_lib, env_fallback

try:
    from linode_api4 import LinodeClient

    HAS_LINODE = True
except ImportError:
    HAS_LINODE = False
    HAS_LINODE_EXC = traceback.format_exc()

COLLECTION_USER_AGENT = 'ansible_linode (https://github.com/linode/ansible_linode) Ansible/{0}'\
    .format(ANSIBLE_VERSION)

LINODE_COMMON_ARGS = dict(
    api_token=dict(
        type='str',
        fallback=(env_fallback, ['LINODE_API_TOKEN', 'LINODE_TOKEN']),
        required=True,
        no_log=True
    ),
    api_version=dict(
        type='str',
        fallback=(env_fallback, ['LINODE_API_VERSION']),
        default='v4'
    ),
    state=dict(
        type='str',
        required=True,
        choices=['present', 'absent'],
    ),
)

LINODE_TAG_ARGS = dict(
    tags=dict(type='list',
              description='The tags to assign to this resource.'),
)

LINODE_LABEL_ARGS = dict(
    label=dict(
        type='str', required=True,
        description='The label to assign to this resource.'),
)


class LinodeModuleBase:
    """A base for all Linode resource modules."""

    def __init__(
            self, module_arg_spec: dict, supports_tags: bool = True, has_label: bool = True,
            bypass_checks: bool = False, no_log: bool = False, mutually_exclusive: Any = None,
            required_together: Any = None, required_one_of: Any = None,
            add_file_common_args: bool = False, supports_check_mode: bool = False,
            required_if: Any = None,
            skip_exec: bool = False) -> None:

        arg_spec = dict()
        arg_spec.update(LINODE_COMMON_ARGS)

        if has_label:
            arg_spec.update(LINODE_LABEL_ARGS)

        if supports_tags:
            arg_spec.update(LINODE_TAG_ARGS)

        arg_spec.update(module_arg_spec)

        self._client = None

        self.module = AnsibleModule(
            argument_spec=arg_spec, bypass_checks=bypass_checks, no_log=no_log,
            mutually_exclusive=mutually_exclusive, required_together=required_together,
            required_one_of=required_one_of, add_file_common_args=add_file_common_args,
            supports_check_mode=supports_check_mode, required_if=required_if)

        self.results: dict = self.results or dict(
            changed=False,
            actions=[]
        )

        if not HAS_LINODE:
            self.fail(msg=missing_required_lib('linode_api4'), exception=HAS_LINODE_EXC)

        if not skip_exec:
            res = self.exec_module(**self.module.params)
            self.module.exit_json(**res)

    def fail(self, msg: str, **kwargs: Any) -> None:
        """
        Shortcut for calling module.fail

        :param msg: Error message
        :param kwargs: Any key=value pairs
        :return: None
        """
        self.module.fail_json(msg=msg, **kwargs)

    def exec_module(self, **kwargs: Any) -> Any:
        """Returns a not implemented error"""
        self.fail("Error: module {0} not implemented".format(self.__class__.__name__))

    def register_action(self, description: str) -> None:
        """Sets the changed flag to true and adds the given action to the result"""

        self.results['changed'] = True
        self.results['actions'].append(description)



    @property
    def client(self) -> LinodeClient:
        """Creates a 'client' property that is used to access the Linode API."""
        if not self._client:
            api_token = self.module.params['api_token']
            api_version = self.module.params['api_version']

            self._client = LinodeClient(
                api_token,
                base_url='https://api.linode.com/{0}'.format(api_version),
                user_agent=COLLECTION_USER_AGENT,
                retry_rate_limit_interval=10,
            )

        return self._client
