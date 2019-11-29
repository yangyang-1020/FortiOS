# Copyright (c) 2015 Fortinet, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

#    FortiOS API request format templates.

# About api request message naming regulations:
# Prefix         HTTP method
# ADD_XXX    -->    POST
# SET_XXX    -->    PUT
# DELETE_XXX -->    DELETE
# GET_XXX    -->    GET

# Login
LOGIN = """
{
    "path": "/logincheck",
    "method": "POST",
    "body": {
        "username": "{{ username }}",
        "secretkey": "{{ secretkey }}"
    }
}
"""

RELOGIN = """login?redir=%2fapi%2fv2"""
LOGOUT = """
{
    "path": "/logout",
    "method": "POST"
}
"""

# Create Interface
ADD_INTERFACE = """
{
    "path": "/api/v2/cmdb/system/interface",
    "method": "POST",
    "body": {
        "json": {
            {% if name is defined %}
                "name": "{{ name }}",
            {% endif %}
            {% if vlanid is defined %}
                "vlanid": "{{ vlanid }}",
            {% endif %}
            "interface": "{{ interface }}",
            "type": "vlan",
            {% if ip is defined %}
                "ip": "{{ ip }}",
                "mode": "static",
                "allowaccess": "ping",
            {% endif %}
            "secondary-IP":"enable",
            {% if alias is defined %}
                "alias": "{{ alias  }}",
            {% endif %}
            {% if vdom is defined %}
                "vdom": "{{ vdom }}",
            {% else %}
                "vdom": "root",
            {% endif %}
            "ipv6": {
                "ip6-extra-addr": []
            }
        }
    }
}
"""

SET_INTERFACE = """
{
    "path": "/api/v2/cmdb/system/interface/{{ name }}",
    "method": "PUT",
    "body": {
        "json": {
            {% if ip is defined and ip != None %}
                "ip": "{{ ip }}",
                "mode": "static",
                "allowaccess": "ping",
            {% endif %}
            {% if secondaryips is defined %}
                {% if secondaryips %}
                    "secondary-IP": "enable",
                    "secondaryip": [
                    {% for secondaryip in secondaryips[:-1] %}
                        {
                            "ip": "{{ secondaryip }}",
                            "allowaccess": "ping"
                        },
                    {% endfor %}
                        {
                            "ip": "{{ secondaryips[-1] }}",
                            "allowaccess": "ping"
                        }
                    ],
                {% else %}
                    "secondary-IP": "disable",
                {% endif %}
            {% endif %}
            {% if vlanid is defined %}
                "vlanid": "{{ vlanid }}",
            {% endif %}
            {% if vdom is defined %}
                "vdom": "{{ vdom }}",
            {% endif %}
            {% if alias is defined %}
                "alias": "{{ alias }}"
            {% else %}
               "alias": "{{ name }}"
            {% endif %}
        }
    }
}
"""

# Delete VLAN (vlan id)
DELETE_INTERFACE = """
{
    {% if vdom is defined %}
        "path":"/api/v2/cmdb/system/interface/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path":"/api/v2/cmdb/system/interface/{{ name }}",
    {% endif %}
    "method": "DELETE"
}
"""

# Get VLAN interface info
GET_INTERFACE = """
{
    {% if name is defined %}
        {% if vdom is defined %}
        "path":"/api/v2/cmdb/system/interface/{{ name }}/?vdom={{ vdom }}",
        {% else %}
        "path":"/api/v2/cmdb/system/interface/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path":"/api/v2/cmdb/system/interface/?vdom={{ vdom }}",
        {% else %}
            "path":"/api/v2/cmdb/system/interface/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# (TODO) remove short-name when 5.6 has a stable release for the fix
ADD_VDOM = """
{
    "path":"/api/v2/cmdb/system/vdom/",
    "method": "POST",
    "body": {
        "json": {
            "short-name": "{{ name }}",
            "name": "{{ name }}"
        }
    }
}
"""

DELETE_VDOM = """
{
    "path":"/api/v2/cmdb/system/vdom/{{ name }}",
    "method": "DELETE"
}
"""

GET_VDOM = """
{
    "path":"/api/v2/cmdb/system/vdom/{{ name }}",
    "method": "GET"
}
"""

ADD_VDOM_LINK = """
{
    "path":"/api/v2/cmdb/system/vdom-link",
    "method": "POST",
    "body": {
        "json": {
            "name":"{{ name }}"
        }
    }
}
"""

DELETE_VDOM_LINK = """
{
    "path": "/api/v2/cmdb/system/vdom-link/{{ name }}",
    "method": "DELETE"
}
"""

GET_VDOM_LINK = """
{
    "path":"/api/v2/cmdb/system/vdom-link/{{ name }}",
    "method": "GET"
}
"""

ADD_ROUTER_STATIC = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/router/static?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/router/static",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            "dst": "{{ dst }}",
            {% if gateway is defined %}
                "gateway": "{{ gateway }}",
            {% endif %}
            "device": "{{ device }}"
        }
    }
}

"""
GET_ROUTER_STATIC6 = """
{
    {% if id is defined %}
        {% if vdom is defined %}
            "path":"/api/v2/cmdb/router/static6/{{ id }}/?vdom={{ vdom }}",
        {% else %}
            "path":"/api/v2/cmdb/router/static6/{{ id }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path":"/api/v2/cmdb/router/static6/?vdom={{ vdom }}",
        {% else %}
            "path":"/api/v2/cmdb/router/static6/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""
ADD_ROUTER_STATIC6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/router/static6?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/router/static6",
    {% endif %}
    "method": "POST",
    "body": {
        "json":{
            "dst": "{{ dst }}",
            {% if gateway is defined %}
                "gateway": "{{ gateway }}"
            {% endif %}
            "device": "{{ device }}"
        }

    }
}
"""

DELETE_ROUTER_STATIC6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/router/static6/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/router/static6/{{ id }}",
    {% endif %}
    "method": "DELETE"
}
"""

SET_ROUTER_STATIC = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/router/static/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/router/static/{{ id }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json":{
            "dst": "{{ dst }}",
            {% if gateway is defined %}
                "gateway": "{{ gateway }}",
            {% endif %}
            "device": "{{ device }}"
        }
    }
}
"""

DELETE_ROUTER_STATIC = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/router/static/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/router/static/{{ id }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_ROUTER_STATIC = """
{
    {% if id is defined %}
        {% if vdom is defined %}
            "path":"/api/v2/cmdb/router/static/{{ id }}/?vdom={{ vdom }}",
        {% else %}
            "path":"/api/v2/cmdb/router/static/{{ id }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path":"/api/v2/cmdb/router/static/?vdom={{ vdom }}",
        {% else %}
            "path":"/api/v2/cmdb/router/static/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

ADD_FIREWALL_POLICY = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/policy?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/policy",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            "srcintf": [
                {
                    {% if srcintf is defined %}
                        "name": "{{ srcintf }}"
                    {% else %}
                        "name": "any"
                    {% endif %}
                }
            ],
            "dstintf": [
                {
                    {% if dstintf is defined %}
                        "name": "{{ dstintf }}"
                    {% else %}
                        "name": "any"
                    {% endif %}
                }
            ],
            "srcaddr":  [
                {
                    {% if srcaddr is defined %}
                        "name": "{{ srcaddr }}"
                    {% else %}
                        "name": "all"
                    {% endif %}
                }
            ],
            "dstaddr":  [
                {
                    {% if dstaddr is defined %}
                        "name": "{{ dstaddr }}"
                    {% else %}
                        "name": "all"
                    {% endif %}
                }
            ],
            {% if action is defined %}
                "action": "{{ action }}",
            {% else %}
                "action": "accept",
            {% endif %}
            "schedule": "always",
            {% if nat is defined %}
            "nat": "{{ nat }}",
            {% endif %}
            {% if poolname is defined %}
                {% if nat is not defined %}
                    "nat": "enable",
                {% endif %}
                "ippool": "enable",
                "poolname":[{
                    "name": "{{ poolname }}"
                }],
            {% endif %}
            {% if match_vip is defined %}
                "match-vip": "{{ match_vip }}",
            {% else %}
                "match-vip": "enable",
            {% endif %}
            {% if status is defined %}
                "status": "{{ status }}",
            {% else %}
                "status": "enable",        "json": {
            {% endif %}
            "service":  [{
                {% if service is defined %}
                    "name": "{{ service }}"
                {% else %}
                    "name": "ALL"
                {% endif %}
            }],
            {% set profiles = {
                'av-profile': av_profile,
                'webfilter-profile': webfilter_profile,
                'ips-sensor': ips_sensor,
                'application-list': application_list,
                'ssl-ssh-profile': ssl_ssh_profile
            } %}
            {% set _utm_enable = true %}
            {% for k, v in profiles.items() if v is defined and v %}
               {% if _utm_enable %}
                   {%set _utm_enable = false %}
                   "utm-status": "enable",
                   "profile-protocol-options":"default",
               {% endif %}
               "{{ k }}": "{{ v }}",
            {% else %}
               "utm-status": "disable",
               "profile-protocol-options": "",
            {% endfor %}
            {% if comments is defined %}
                "comments": "{{ comments }}"
            {% else %}
                "comments": ""
            {% endif %}
        }
    }
}
"""

SET_FIREWALL_POLICY = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {
            {% if srcintf is defined %}
                "srcintf": [
                    {
                        "name": "{{ srcintf }}"
                    }
                ],
            {% endif %}
            {% if dstintf is defined %}
                "dstintf": [
                    {
                        "name": "{{ dstintf }}"
                    }
                ],
            {% endif %}
            {% if srcaddr is defined %}
                "srcaddr":  [
                    {
                        "name": "{{ srcaddr }}"
                    }
                ],
            {% endif %}
            {% if dstaddr is defined %}
                "dstaddr":  [
                    {
                        "name": "{{ dstaddr }}"
                    }
                ],
            {% endif %}
            {% if action is defined %}
                "action": "{{ action }}",
            {% endif %}
            {% if nat is defined %}
            "nat": "{{ nat }}",
            {% endif %}
            {% if poolname is defined %}
                {% if nat is not defined %}
                    "nat": "enable",
                {% endif %}
                "ippool": "enable",
                "poolname":[{
                    "name":"{{ poolname }}"
                }],
            {% endif %}
            {% if match_vip is defined %}
                "match-vip":"{{ match_vip }}",
            {% endif %}
            {% if status is defined %}
                "status":"{{ status }}",
            {% endif %}
            {% if service is defined %}
                "service":  [{
                    "name": "{{ service }}"
                }],
            {% endif %}
            {% set profiles = {
                'av-profile': av_profile,
                'webfilter-profile': webfilter_profile,
                'ips-sensor': ips_sensor,
                'application-list': application_list,
                'ssl-ssh-profile': ssl_ssh_profile
            } %}
            {% set _utm_enable = true %}
            {% for k, v in profiles.iteritems() if v is defined and v is not none %}
               {% if _utm_enable %}
                   {%set _utm_enable = false %}
                   "utm-status": "enable",
                   "profile-protocol-options":"default",
               {% endif %}
               "{{ k }}": "{{ v }}",
            {% else %}
               "utm-status": "disable",
               "profile-protocol-options": "",
            {% endfor %}
            {% if comments is defined %}
                "comments": "{{ comments }}",
            {% endif %}
            "schedule": "always"
        }
    }
}
"""

DELETE_FIREWALL_POLICY = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_POLICY = """
{
    {% if id is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/policy/{{ id }}?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/policy/{{ id }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/policy/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/policy/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

MOVE_FIREWALL_POLICY = """
{
    {% if vdom is defined %}
        {% if before is defined %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}?vdom={{ vdom }}&action=move&before={{ before }}",
        {% else %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}?vdom={{ vdom }}&action=move&after={{ after }}",
        {% endif %}
    {% else %}
        {% if before is defined %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}?action=move&before={{ before }}",
        {% else %}
        "path": "/api/v2/cmdb/firewall/policy/{{ id }}?action=move&after={{ after }}",
        {% endif %}
    {% endif %}
    "method": "PUT"
}
"""

ADD_FIREWALL_POLICY6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/policy6?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/policy6",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            "srcintf": [
                {
                    {% if srcintf is defined %}
                        "name": "{{ srcintf }}"
                    {% else %}
                        "name": "any"
                    {% endif %}
                }
            ],
            "dstintf": [
                {
                    {% if dstintf is defined %}
                        "name": "{{ dstintf }}"
                    {% else %}
                        "name": "any"
                    {% endif %}
                }
            ],
            "srcaddr":  [
                {
                    {% if srcaddr is defined %}
                        "name": "{{ srcaddr }}"
                    {% else %}
                        "name": "all"
                    {% endif %}
                }
            ],
            "dstaddr":  [
                {
                    {% if dstaddr is defined %}
                        "name": "{{ dstaddr }}"
                    {% else %}
                        "name": "all"
                    {% endif %}
                }
            ],
            {% if action is defined %}
                "action": "{{ action }}",
            {% else %}
                "action": "accept",
            {% endif %}
            "schedule": "always",
            {% if nat is defined %}
            "nat": "{{ nat }}",
            {% endif %}
            {% if poolname is defined %}
                {% if nat is not defined %}
                    "nat": "enable",
                {% endif %}
                "ippool": "enable",
                "poolname":[{
                    "name": "{{ poolname }}"
                }],
            {% endif %}
            {% if match_vip is defined %}
                "match-vip": "{{ match_vip }}",
            {% else %}
                "match-vip": "enable",
            {% endif %}
            {% if status is defined %}
                "status": "{{ status }}",
            {% else %}
                "status": "enable",
            {% endif %}
            "service":  [{
                {% if service is defined %}
                    "name": "{{ service }}"
                {% else %}
                    "name": "ALL"
                {% endif %}
            }],
            {% set profiles = {
                'av-profile': av_profile,
                'webfilter-profile': webfilter_profile,
                'ips-sensor': ips_sensor,
                'application-list': application_list,
                'ssl-ssh-profile': ssl_ssh_profile
            } %}
            {% set _utm_enable = true %}
            {% for k, v in profiles.iteritems() if v is defined and v %}
               {% if _utm_enable %}
                   {%set _utm_enable = false %}
                   "utm-status": "enable",
                   "profile-protocol-options":"default",
               {% endif %}
               "{{ k }}": "{{ v }}",
            {% else %}
               "utm-status": "disable",
               "profile-protocol-options": "",
            {% endfor %}
            {% if comments is defined %}
                "comments": "{{ comments }}"
            {% else %}
                "comments": ""
            {% endif %}
        }
    }
}
"""

SET_FIREWALL_POLICY6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {
            {% if srcintf is defined %}
                "srcintf": [
                    {
                        "name": "{{ srcintf }}"
                    }
                ],
            {% endif %}
            {% if dstintf is defined %}
                "dstintf": [
                    {
                        "name": "{{ dstintf }}"
                    }
                ],
            {% endif %}
            {% if srcaddr is defined %}
                "srcaddr":  [
                    {
                        "name": "{{ srcaddr }}"
                    }
                ],
            {% endif %}
            {% if dstaddr is defined %}
                "dstaddr":  [
                    {
                        "name": "{{ dstaddr }}"
                    }
                ],
            {% endif %}
            {% if action is defined %}
                "action": "{{ action }}",
            {% endif %}
            {% if nat is defined %}
            "nat": "{{ nat }}",
            {% endif %}
            {% if poolname is defined %}
                {% if nat is not defined %}
                    "nat": "enable",
                {% endif %}
                "ippool": "enable",
                "poolname":[{
                    "name":"{{ poolname }}"
                }],
            {% endif %}
            {% if match_vip is defined %}
                "match-vip":"{{ match_vip }}",
            {% endif %}
            {% if status is defined %}
                "status":"{{ status }}",
            {% endif %}
            {% if service is defined %}
                "service":  [{
                    "name": "{{ service }}"
                }],
            {% endif %}
            {% set profiles = {
                'av-profile': av_profile,
                'webfilter-profile': webfilter_profile,
                'ips-sensor': ips_sensor,
                'application-list': application_list,
                'ssl-ssh-profile': ssl_ssh_profile
            } %}
            {% set _utm_enable = true %}
            {% for k, v in profiles.iteritems() if v is defined and v is not none %}
               {% if _utm_enable %}
                   {%set _utm_enable = false %}
                   "utm-status": "enable",
                   "profile-protocol-options":"default",
               {% endif %}
               "{{ k }}": "{{ v }}",
            {% else %}
               "utm-status": "disable",
               "profile-protocol-options": "",
            {% endfor %}
            {% if comments is defined %}
                "comments": "{{ comments }}",
            {% endif %}
            "schedule": "always"
        }
    }
}
"""

DELETE_FIREWALL_POLICY6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_POLICY6 = """
{
    {% if id is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/policy6/{{ id }}?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/policy6/{{ id }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/policy6/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/policy6/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

MOVE_FIREWALL_POLICY6 = """
{
    {% if vdom is defined %}
        {% if before is defined %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}?vdom={{ vdom }}&action=move&before={{ before }}",
        {% else %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}?vdom={{ vdom }}&action=move&after={{ after }}",
        {% endif %}
    {% else %}
        {% if before is defined %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}?action=move&before={{ before }}",
        {% else %}
        "path": "/api/v2/cmdb/firewall/policy6/{{ id }}?action=move&after={{ after }}",
        {% endif %}
    {% endif %}
    "method": "PUT"
}
"""

ADD_FIREWALL_VIP = """
{
    {% if vdom is defined %}
        "path":"/api/v2/cmdb/firewall/vip?vdom={{ vdom }}",
    {% else %}
        "path":"/api/v2/cmdb/firewall/vip",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            "name": "{{ name }}",
            "extip": "{{ extip }}",
            "extintf": "{{ extintf }}",
            "mappedip": [
            {
                    "range": "{{ mappedip }}"
            }
            ]
        }
    }
}
"""

DELETE_FIREWALL_VIP = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/vip/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/vip/{{ name }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_VIP = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/vip/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/vip/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/vip/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/vip/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

ADD_FIREWALL_IPPOOL = """
{
    {% if vdom is defined %}
        "path":"/api/v2/cmdb/firewall/ippool?vdom={{ vdom }}",
    {% else %}
        "path":"/api/v2/cmdb/firewall/ippool",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            "startip": "{{ startip }}",
            {% if endip is defined %}
                "endip": "{{ endip }}",
            {% else %}
                "endip": "{{ startip }}",
            {% endif %}
            {% if type is defined %}
                "type": "{{ type }}",
            {% else %}
                "type": "one-to-one",
            {% endif %}
            {% if comments is defined %}
                "comments": "{{ comments }}",
            {% endif %}
            {% if name is defined %}
                "name": "{{ name }}"
            {% else %}
                "name": "{{ startip }}"
            {% endif %}
        }
    }
}
"""

DELETE_FIREWALL_IPPOOL = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/ippool/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/ippool/{{ name }}/",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_IPPOOL = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/ippool/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/ippool/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/ippool/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/ippool/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

## firewall addresses
ADD_FIREWALL_ADDRESS = """
{
    {% if vdom is defined %}
        "path":"/api/v2/cmdb/firewall/address?vdom={{ vdom }}",
    {% else %}
        "path":"/api/v2/cmdb/firewall/address",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            {% if associated_interface is defined %}
                "associated-interface": "{{ associated_interface }}",
            {% endif %}
            {% if comment is defined %}
                "comment": "{{ comment }}",
            {% endif %}
            "subnet": "{{ subnet }}",
            "name": "{{ name }}"
        }
    }
}
"""

ADD_FIREWALL_ADDRESS6 = """
{
    {% if vdom is defined %}
        "path":"/api/v2/cmdb/firewall/address6?vdom={{ vdom }}",
    {% else %}
        "path":"/api/v2/cmdb/firewall/address6",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            {% if associated_interface is defined %}
                "associated-interface": "{{ associated_interface }}",
            {% endif %}
            {% if comment is defined %}
                "comment": "{{ comment }}",
            {% endif %}
            "ip6": "{{ subnet }}",
            "name": "{{ name }}"
        }
    }
}
"""

SET_FIREWALL_ADDRESS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/address/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/address/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {
            {% if associated_interface is defined %}
                "associated-interface": "{{ associated_interface }}",
            {% endif %}
            {% if comment is defined %}
                "comment": "{{ comment }}",
            {% endif %}
            {% if subnet is defined %}
                "subnet": "{{ subnet }}",
            {% endif %}
            "name": "{{ name }}"
        }
    }
}
"""

SET_FIREWALL_ADDRESS6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/address6/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/address6/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {
            {% if associated_interface is defined %}
                "associated-interface": "{{ associated_interface }}",
            {% endif %}
            {% if comment is defined %}
                "comment": "{{ comment }}",
            {% endif %}
            {% if subnet is defined %}
                "subnet": "{{ subnet }}",
            {% endif %}
            "name": "{{ name }}"
        }
    }
}
"""

DELETE_FIREWALL_ADDRESS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/address/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/address/{{ name }}",
    {% endif %}
    "method": "DELETE"
}
"""

DELETE_FIREWALL_ADDRESS6 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/address6/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/address6/{{ name }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_ADDRESS = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/address/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/address/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/address/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/address/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

GET_FIREWALL_ADDRESS6 = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/address6/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/address6/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/address6/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/address6/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

## firewall address group
ADD_FIREWALL_ADDRGRP = """
{
    {% if vdom is defined %}
        "path":"/api/v2/cmdb/firewall/addrgrp?vdom={{ vdom }}",
    {% else %}
        "path":"/api/v2/cmdb/firewall/addrgrp/",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            "name": "{{ name }}",
            "member": [
            {% for member in members[:-1] %}
                {
                    "name": "{{ member }}"
                },
            {% endfor %}
                {
                    "name": "{{ members[-1] }}"
                }
            ]
        }
    }
}
"""

SET_FIREWALL_ADDRGRP = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/addrgrp/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/addrgrp/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
            "member": [
            {% for member in members[:-1] %}
                {
                    "name": "{{ member }}"
                },
            {% endfor %}
                {
                    "name": "{{ members[-1] }}"
                }
            ]
    }
}
"""

DELETE_FIREWALL_ADDRGRP = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/addrgrp/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/addrgrp/{{ name }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_ADDRGRP = """
{
    {% if vdom is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/addrgrp/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/addrgrp/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall/addrgrp/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall/addrgrp/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

## firewall service custom
ADD_FIREWALL_SERVICE = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.service/custom?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.service/custom",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            {% if protocol is defined %}
                "protocol": "{{ protocol }}",
            {% else %}
                "protocol": "TCP/UDP/SCTP",
            {% endif %}
            {% if fqdn is defined %}
                "fqdn": "{{ fqdn }}",
            {% endif %}
            {% if iprange is defined %}
                "iprange": "{{ iprange }}",
            {% endif %}
            {% if tcp_portrange is defined %}
                "tcp-portrange": "{{ tcp_portrange }}",
            {% endif %}
            {% if udp_portrange is defined %}
                "udp-portrange": "{{ udp_portrange }}",
            {% endif %}
            {% if sctp_portrange is defined %}
                "sctp-portrange": "{{ udp_portrange }}",
            {% endif %}
            {% if comment is defined %}
                "comment": "{{ comment }}",
            {% endif %}
            "name": "{{ name }}"
        }
    }
}
"""

## update firewall service custom
SET_FIREWALL_SERVICE = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.service/custom/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.service/custom/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {
            {% if protocol is defined %}
                "protocol": "{{ protocol }}",
            {% endif %}
            {% if fqdn is defined %}
                "fqdn": "{{ fqdn }}",
            {% endif %}
            {% if iprange is defined %}
                "iprange": "{{ iprange }}",
            {% endif %}
            {% if tcp_portrange is defined %}
                "tcp-portrange": "{{ tcp_portrange }}",
            {% else %}
                "tcp-portrange": "",
            {% endif %}
            {% if udp_portrange is defined %}
                "udp-portrange": "{{ udp_portrange }}",
            {% else %}
                "udp-portrange": "",
            {% endif %}
            {% if sctp_portrange is defined %}
                "sctp-portrange": "{{ sctp_portrange }}",
            {% else %}
                "sctp-portrange": "",
            {% endif %}
            {% if comment is defined %}
                "comment": "{{ comment }}",
            {% endif %}
            "name": "{{ name }}"
        }
    }
}
"""

DELETE_FIREWALL_SERVICE = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.service/custom/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.service/custom/{{ name }}",
    {% endif %}
    "method": "DELETE"
}
"""

GET_FIREWALL_SERVICE = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall.service/custom/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall.service/custom/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall.service/custom/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall.service/custom/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

## get firewall service group
GET_FIREWALL_SERVICE_GROUP = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall.service/group/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall.service/group/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/firewall.service/group/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/firewall.service/group/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# requirement for splunk AR plugin to revoke user
GET_USER_GROUP = """
{
    {% if name is defined %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/user/group/{{ name }}/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/user/group/{{ name }}/",
        {% endif %}
    {% else %}
        {% if vdom is defined %}
            "path": "/api/v2/cmdb/user/group/?vdom={{ vdom }}",
        {% else %}
            "path": "/api/v2/cmdb/user/group/",
        {% endif %}
    {% endif %}
    "method": "GET"

}
"""

PUT_USER_GROUP = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/group/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/group/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {
            {% if member| length > 0 %}
            "member": [
                {% for m in member[:-1] %}
                {
                    "name": "{{ m }}",
                    "q_origin_key": "{{ m }}"
                },
                {% endfor %}
                {
                    "name": "{{ member[-1] }}",
                    "q_origin_key": "{{ member[-1] }}"
                }
            ],
            {% else %}
            "member": [],
            {% endif %}
            "name": "{{ name }}"
        }
    }
}

"""

ADD_VPN_P1_TEST = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb//vpn.ipsec/phase1-interface?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb//vpn.ipsec/phase1-interface",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            
            "name": "{{ name }}",
            "type": "{{ type }}",
            "interface": "{{ interface }}",
            "ip-version": 4,
            "ike-version": {{ ike_version }},
            "remote-gw": "{{ remote_gw }}",
            "keylife": {{ keylife }}
        }
    }
}
"""

ADD_VPN_P1 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase1-interface?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase1-interface",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {

            "name": "{{ name }}",
            "type": "{{ type }}",
            "interface": "{{ interface }}",
            "ip-version": 4,
            "ike-version": {{ ike_version }},
            "remote-gw": "{{ remote_gw }}",
            "keylife": {{ keylife }},
            "authmethod": "psk",
            "mode": "{{ mode }}",
            "peertype": "any",
            "proposal": "{{ p1proposal }}",
            "keepalive": {{ keepalive }},
            "dhgrp": {{ dhgrp }},
            "psksecret":"{{ psksecret }}",
            {% if comments  %}
                "comments": "{{ comments }}"

            {% else %}
                "comments": ""
            {% endif %}

        }
    }
}
"""

SET_VPN_P1 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb//vpn.ipsec/phase1-interface/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb//vpn.ipsec/phase1-interface/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {

                {% if interface is defined %}
                    "interface": "{{ interface }}",
                {% endif %}

                {% if remote_gw is defined %}
                    "remote-gw": "{{ remote_gw }}",
                {% endif %}

                {% if keylife is defined %}
                    "keylife": {{ keylife }},
                {% endif %}

                {% if mode is defined %}
                    "mode": "{{ mode }}",
                {% endif %}

                {% if p1proposal is defined %}
                    "proposal": "{{ proposal }}",
                {% endif %}

                {% if keepalive is defined %}
                    "keepalive": {{ keepalive }},
                {% endif %}

                {% if dhgrp is defined %}
                    "dhgrp": {{ dhgrp }},
                {% endif %}

                {% if psksecret is defined %}
                    "psksecret":"{{ psksecret }}",
                {% endif %}


                {% if comments  %}
                    "comments": "{{ comments }}"

                {% else %}
                    "comments": ""
                {% endif %}


        }
    }
}

"""

DELETE_VPN_P1 = """
{
 {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase1-interface/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase1-interface/{{ name }}",
    {% endif %}
    "method": "DELETE"

}
"""

GET_VPN_P1 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase1-interface/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase1-interface/{{name}}",
    {% endif %}

    "method": "GET"
}
"""

ADD_VPN_P2 = """

{


    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase2-interface?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase2-interface",   
    {% endif %}

    "method": "POST",

    "body": {
        "json": {

            "name": "{{ name }}",
            "phase1name": "{{ phase1name }}",
            "proposal": "{{ proposal }}",
            "pfs": "{{ pfs }}",
            "dhgrp": "{{ dhgrp }}",

            {% if replay %}
                "replay": "{{ replay }}",
            {% else %}
                "replay": "enable",

            {% endif %}  


            {% if keepalive %}
                "keepalive": "{{ keepalive }}",
            {% else %}
                "keepalive": "enable",

            {% endif %}

            {% if auto_negotiate %}
                "auto-negotiate": "{{ auto_negotiate }}",
            {% else %}
                "auto-negotiate": "enable",

            {% endif %}



            {% if keylife_type %}

                {% if keylife_type == "seconds" %}

                    "keylife-type": "seconds",

                    {% if keylifeseconds %}
                        "keylifeseconds": "{{ keylifeseconds }}",

                    {% endif %}

                {% elif keylife_type == "kbps" %}
                     "keylife-type": "kbps",
                    {% if keylifekbs %}
                            "keylifekbs": "{{ keylifekbs }}",

                    {% endif %}

                {% else %}
                    "keylife-type": "both",

                    {% if keylifeseconds %}
                        "keylifeseconds": "{{ keylifeseconds }}",

                    {% endif %}

                    {% if keylifekbs %}

                            "keylifekbs": "{{ keylifekbs }}",

                    {% endif %}
                {% endif %}



            {% else %}
                "keylife-type": "seconds",

            {% endif %}

            "src-addr-type": "subnet",
            "src-subnet": "{{ src_subnet }}",

            "dst-subnet": "{{ dst_subnet }}",

            "dst-addr-type": "subnet"




        }

    }
}

"""

SET_VPN_P2 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb//vpn.ipsec/phase2-interface/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb//vpn.ipsec/phase2-interface/{{ name }}",
    {% endif %}
    "method": "PUT",
    "body": {
        "json": {

            {% if phase1name %}
                "phase1name": "{{ phase1name }}",
            {% endif %}

            {% if proposal %}
                "proposal": "{{ proposal }}",
            {% endif %}

            {% if pfs %}
                "pfs": "{{ pfs }}",
            {% endif %}



            {% if dhgrp %}
                "dhgrp": "{{ dhgrp }}",
            {% endif %}



            {% if replay %}
                "replay": "{{ replay }}",
            {% endif %}  


            {% if keepalive %}
                "keepalive": "{{ keepalive }}",

            {% endif %}

            {% if auto_negotiate %}
                "auto-negotiate": "{{ auto_negotiate }}",

            {% endif %}



            {% if keylife_type %}

                {% if keylife_type == "seconds" %}

                    "keylife-type": "seconds",

                    {% if keylifeseconds %}
                        "keylifeseconds": "{{ keylifeseconds }}",

                    {% endif %}

                {% elif keylife_type == "kbps" %}
                     "keylife-type": "kbps",
                    {% if keylifekbs %}
                            "keylifekbs": "{{ keylifekbs }}",

                    {% endif %}

                {% endif %}




            {% endif %}


             {% if src_subnet %}
                "src-subnet": "{{ src_subnet }}",

            {% endif %}            

             {% if dst_subnet %}
                "dst-subnet": "{{ dst_subnet }}",

            {% endif %}

            {% if comments  %}
                    "comments": "{{ comments }}"

            {% else %}
                    "comments": ""
            {% endif %}




        }

    }
}

"""

DELETE_VPN_P2 = """
{
 {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase2-interface/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase2-interface/{{ name }}",
    {% endif %}
    "method": "DELETE"

}
"""

GET_VPN_P2 = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase2-interface?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ipsec/phase2-interface",
    {% endif %}

    "method": "GET"
}

"""

ADD_TRAFFIC_SHAPERS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper",
    {% endif %}
    
    "method": "POST",
    "body": {
        "json": {
            "name": "{{ name }}",
            "maximum-bandwidth": {{ bandwidth }},
            "bandwidth-unit": "kbps",
            "priority": "high",
            "per-policy": "enable"
            
            }    
    }
}

"""

SET_TRAFFIC_SHAPERS = """

{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper/{{ name }}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper/{{ name }}",
    {% endif %}
    
    "method": "PUT",
    
    "body": {
        "json": {
        
            "maximum-bandwidth": {{ bandwidth }}
            
            }  
            
        }
        
}


"""

DELETE_TRAFFIC_SHAPERS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper/{{ name }}",
    {% endif %}
    "method": "DELETE"
    
}
"""

GET_TRAFFIC_SHAPERS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper",
    {% endif %}
    
    "method": "GET"
}
"""

ADD_TRAFFIC_POLICY = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/shaping-policy?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/shaping-policyr",
    {% endif %}
    
    "method": "POST",
    "body": {
        "json": {
        
            "id":{{ id }} ,
            "status": "enable",
            
            "ip-version": {{ ipversion }},
            
            "srcaddr": [
                {
                    "name": "{{ srcaddr }}"
                }
            ],
            "dstaddr": [
                {
                    "name": "{{ dstaddr }}"
                }
            ],
            "service": [
                {
                    "name": "{{ service }}"
                }
            ],
            "dstintf": [
                {
                    "name": "{{ dstintf }}"
                }
            ],
            "traffic-shaper": "{{ traffic_shaper }}",
            "traffic-shaper-reverse": "{{ traffic_shaper_revers }}",
            
            {% if comments %}
                "comments": "{{ comments }}"
            {% else %}
                "comments": ""
            {% endif %}
       
            
        }    
    }
}

"""

SET_TRAFFIC_POLICY = """

{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper/{{ id }}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall.shaper/traffic-shaper/{{ id }}",
    {% endif %}
    
    "method": "PUT",
    
    "body": {
        "json": {
            
           
            
            {% if status %}
                "status": "{{ status }}",
            {% else %}
            
            {% endif %}
            
            {% if ipversion %}
                "ip-version": {{ ipversion }},
            {% else %}
            
            {% endif %}
            
            {% if srcaddr %}
                "srcaddr": [
                    {
                        "name": "{{ srcaddr }}"
                    }
                ],
             
            
            {% else %}
            
            {% endif %}
            
            {% if dstaddr %}
             
                "dstaddr": [
                    {
                    "name": "{{ dstaddr }}"
                    }
                ],
            
            {% else %}
            
            {% endif %}
            
            
            
            
            
            {% if service %}
            
                 "service": [
                {
                    "name": "{{ service }}"
                }
            ],
            
            {% else %}
            
            {% endif %}
            
            
            
            {% if dstintf %}
                
                "dstintf": [
                    {
                        "name": "{{ dstintf }}"
                    }
                ],
            
            {% else %}
            
            {% endif %}
            
            
            {% if traffic_shaper %}
                "traffic-shaper": "{{ traffic_shaper }}",
            {% else %}
            
            {% endif %}
            
             
            {% if traffic_shaper_revers %}
             
              "traffic-shaper-reverse": "{{ traffic_shaper_revers }}",
            
            {% else %}
            
            {% endif %}
            
            
           
            
            {% if comments %}
                "comments": "{{ comments }}"
            {% else %}
                "comments": ""
            {% endif %}
            
            }  
            
        }
        
}
"""

DELETE_TRAFFIC_POLICY = """
{
 {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/shaping-policy/{{ id }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/shaping-policy/{{ id }}",
    {% endif %}
    "method": "DELETE"
    
}
"""

GET_TRAFFIC_POLICY = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/shaping-policy?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/shaping-policy",
    {% endif %}
    
    "method": "GET"
}
"""

GET_ROUTING_TABLE = """
{
    {% if vdom is defined %}
        "path": "/api/v2/monitor/router/ipv4/select/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/monitor/router/ipv4/select/",
    {% endif %}    
    "method": "GET"
}
"""

GET_IPSEC_STATIUS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/monitor/vpn/ipsec/select/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/monitor/vpn/ipsec/select/",
    {% endif %}   
    "method": "GET"
}
"""

GET_HA_STATIUS = """
{
    {% if vdom is defined %}
        "path": "/api/v2/monitor/system/ha-statistics/select/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/monitor/system/ha-statistics/select/",
    {% endif %}   
    "method": "GET"
}
"""

GET_Interface_Select = """
{
    {% if vdom is defined %}
        "path": "/api/v2/monitor/system/interface/select/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/monitor/system/interface/select/",
    {% endif %}   
    "method": "GET"
}
"""
GET_SYSTEM_UseRange = """
{
    "path": "/api/v2/monitor/system/resource/usage", 
    "method": "GET"
}
"""


GET_Bandwidth_USED = """
{
    "path": "/api/v2/monitor/system/traffic-history?interface={{port}}&time_period={{time}}",  
    "method": "GET"
}
"""

GET_Interface_Status = """
{
    "path": "/api/v2/monitor/system/available-interfaces?scope=global",  
    "method": "GET"
}
"""


#SSL VPN service

GET_VPN_SSL_Settings="""
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl/settings?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl/settings",
    {% endif %}   
    "method": "GET"
}
"""

PUT_VPN_SSL_Settings="""
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl/settings?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl/settings",
    {% endif %}   
    "method": "PUT",
    "body": {
        "json": {
                {% if port %}
                "port": {{ port }},
                {% else %}
                {% endif %}                
                "http-request-body-timeout": 30
              
        }    
    }
}
"""

#SSL VPN Policy
GET_VPN_SSL_Policy = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal/{{name}}",
    {% endif %}   
    "method": "GET"
}
"""

ADD_VPN_SSL_Policy = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal",
    {% endif %}   
    "method": "POST"
    "body": {
        "json": {
              "name": {{ name }},
              "tunnel-mode": "enable",
              "ip-mode": "range",
              "ip-pools": [
                {
                  "name": {{ ip-pool }}
                }
              ],
              "web-mode": "disable"
            }
        }
}
"""

PUT_VPN_SSL_Policy = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal/{{name}}",
    {% endif %}   
    "method": "PUT"
    "body": {
        "json": {
              "ip-pools": [
                        {
                          "name": {{ ip-pool }}
                        }
                      ]
                }
             }   
}
"""



DEL_VPN_SSL_Policy = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl.web/portal/{{name}}",
    {% endif %}   
    "method": "DELETE"
}
"""



# USERS

GET_LOCAl_USER = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/local/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/local/{{name}}",
    {% endif %}   
    "method": "GET"
}
"""

ADD_LOCAl_USER = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/local/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/local/",
    {% endif %}   
    "method": "POST"
    "body": {
        "json": {
            "name": {{name}},
            "passwd": {{ passwd }},
             "status": {{ status }},
             "type": "password"
                }
            } 
}
"""

PUT_LOCAl_USER = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/local/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/local/{{name}}",
    {% endif %}   
    "method": "PUT"
    "body": {
        "json": {
            "passwd": {{ passwd }},
             "status": {{ status }},
             "type": "password"
                }
            } 
}
"""

DEL_LOCAl_USER = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/local/{{name}}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/local/{{name}}",
    {% endif %}   
    "method": "GET"
}
"""

# USER GROUP

ADD_USER_GROUP = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/group/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/group/{{ name }}",
    {% endif %}
    "method": "POST",
    "body": {
        "json": {
            {% if member| length > 0 %}
            "member": [
                {% for m in member[:-1] %}
                {
                    "name": "{{ m }}",
                    "q_origin_key": "{{ m }}"
                },
                {% endfor %}
                {
                    "name": "{{ member[-1] }}",
                    "q_origin_key": "{{ member[-1] }}"
                }
            ],
            {% else %}
            "member": [],
            {% endif %}
            "name": "{{ name }}"
        }
    }
}

"""

DEL_USER_GROUP = """
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/user/group/{{ name }}/?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/user/group/{{ name }}",
    {% endif %}
    "method": "DELETE",

"""

VPN_SSL_Bind = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/vpn.ssl/settings?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/vpn.ssl/settings",
    {% endif %}   
    "method": "PUT",
    "body": {
        "json": {
                "authentication-rule": [
                      {
                        "id": 1,
                        "source-interface": [
                          {
                            "name": "port1"
                          }
                        ],
                        "source-address": [
                          {
                            "name": "all"
                          }
                        ],
                        "users": [
                          {
                            "name": "test"
                          },
                          {
                            "name": "guest"
                          }
                        ],
                        "groups": [
                          {
                            "name": "ssl"
                          },
                          {
                            "name": "Guest-group"
                          }
                        ]
                      }
                    ]
              
        }    
    }
}
"""

get_central_snat_map = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/central-snat-map/{{ policyid }}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/central-snat-map/{{ policyid }}",
    {% endif %}   
    "method": "GET"
}
"""

del_central_snat_map = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/central-snat-map/{{ policyid }}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/central-snat-map/{{ policyid }}",
    {% endif %}   
    "method": "DELETE"
}
"""
add_central_snat_map = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/central-snat-map?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/central-snat-map",
    {% endif %}   
    "method": "POST",
    "body": {
        "json": {
            "policyid": 0,
            "status": "enable",
            "orig-addr": [
                {
                  "name": "{{ orig_addr }}"
                }
            ],
            "srcintf": [
                {
                  "name": "{{ srcintf }}"
                }
            ],
            "dst-addr": [
                {
                  "name": "{{ dst_addr }}"
                }
            ],
            "dstintf": [
                {
                  "name": "{{ dstintf }}"
                }
            ],
            "nat-ippool": [
                {
                  "name": "{{ ippool }}"
                }
            ],
            {% if comments %}
                "comments": "{{ comments }}"
            {% else %}
                "comments": ""
            {% endif %}
        }
    }
}
"""

set_central_snat_map = """
{
    {% if vdom is defined %}
        "path": "/api/v2/cmdb/firewall/central-snat-map/{{ policyid }}?vdom={{ vdom }}",
    {% else %}
        "path": "/api/v2/cmdb/firewall/central-snat-map/{{ policyid }}",
    {% endif %}   
    "method": "PUT",
    "body": {
        "json": {
            {% if orig_addr is defined %}
                "orig-addr": [
                    {
                      "name": "{{ orig_addr }}"
                    }
                ],
            {% endif %}
            {% if srcintf is defined %}
                "srcintf": [
                    {
                      "name": "{{ srcintf }}"
                    }
                ],
            {% endif %}
            {% if dst_addr is defined %}
                "dst-addr": [
                    {
                      "name": "{{ dst_addr }}"
                    }
                ],
            {% endif %}
            {% if dstintf is defined %}
                "dstintf": [
                    {
                      "name": "{{ dstintf }}"
                    }
                ],
            {% endif %}
            {% if ippool is defined %}   
                "nat-ippool": [
                    {
                      "name": "{{ ippool }}"
                    }
                ],
            {% endif %}
            {% if comments %}
                "comments": "{{ comments }}"
            {% else %}
                "comments": ""
            {% endif %}
        }
    }
}
"""




