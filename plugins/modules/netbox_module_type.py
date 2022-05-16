#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_module_type
short_description: Create, update or delete module types within NetBox
description:
  - Creates, updates or removes module types from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)/Mika Doerr
requirements:
  - pynetbox
version_added: '0.1.0'
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    description:
      - Defines the module type configuration
    suboptions:
      manufacturer:
        description:
          - The manufacturer of the module type.
        required: true
        type: raw
      model:
        description:
          - The model of the module type
        required: true
        type: str
      part_number:
        description:
          - The part number of the module type.
        required: false
        type: str
      comments:
        description:
          - The comments of the associated module type.
        required: false
        type: str
      tags:
        description:
          - Any tags that the module type may need to be associated with
        required: false
        type: list
        elements: raw
    type: dict
    required: true
"""

EXAMPLES = r"""
- name: "Test NetBox modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create module type within NetBox with only required information
      netbox_module_type:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          manufacturer: Test Manufacturer One
          model: "Module type model One"
        state: present

    - name: Delete module type within netbox
      netbox_module_type:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          model: "Module type model One"
        state: absent

"""

RETURN = r"""
module_type:
  description: Serialized object as created or already existent within NetBox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_dcim import (
    NetboxDcimModule,
    NB_MODULE_TYPES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    manufacturer=dict(required=True, type="raw"),
                    model=dict(required=True, type="str"),
                    part_number=dict(required=False, type="str"),
                    comments=dict(required=False, type="str"),
                    tags=dict(required=False, type="list", elements="raw"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["manufacturer"]), ("state", "absent", ["manufacturer"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_module_type = NetboxDcimModule(module, NB_MODULE_TYPES)
    netbox_module_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
