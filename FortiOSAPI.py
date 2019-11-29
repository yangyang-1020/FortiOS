import json
import logging
import urllib

import jinja2
import requests

from templates import *

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# may need to move to specifying the ca or use Verify=false
# verify="/etc/ssl/certs/" on Debian to use the system CAs
logging.getLogger(__name__).addHandler(NullHandler())
# create logger
LOG = logging.getLogger('fortiosapi')


class FClient(object):

    def __init__(self):
        self.host = None
        self._https = False
        self._logged = False
        self._fortiversion = "Version is set when logged"
        # reference the fortinet version of the targeted product.
        self._session = requests.session()  # use single session
        # persistant and same for all
        self._session.verify = False
        # (can be changed to) self._session.verify = '/etc/ssl/certs/' or True
        # Will be switch to true by default it uses the python CA list in this case
        self.timeout = 10
        self.cert = None
        self._apitoken = None
        self._license = None
        self.url_prefix = None

    def login(self, host, username, password, verify=False, cert=None, timeout=12, https=None,):
        self.host = host
        LOG.debug("self._https is %s", self._https)

        self._https = https
        if not self._https:
            self.url_prefix = 'http://' + self.host
        else:
            self.url_prefix = 'https://' + self.host

        url = self.url_prefix + '/logincheck'
        if not self._session:
            self._session = requests.session()
            # may happen if logout is called
        if verify is not False:
            self._session.verify = verify

        if cert is not None:
            self._session.cert = cert
        # set the default at 12 see request doc for details http://docs.python-requests.org/en/master/user/advanced/
        self.timeout = timeout

        res = self._session.post(
            url,
            data='username=' + urllib.request.pathname2url(username) + '&secretkey=' + urllib.request.pathname2url(
                password) + "&ajax=1",
            timeout=self.timeout)
        self.logging(res)
        # Ajax=1 documented in 5.6 API ref but available on 5.4
        LOG.debug("logincheck res : %s", res.content)
        if res.content.decode('ascii')[0] == '1':
            # Update session's csrftoken
            self.update_cookie()
            self._logged = True
            return True
        else:
            self._logged = False
            raise Exception('login failed')

    def logout(self):
        try:
            url = self.url_prefix + '/logout'
            res = self._session.post(url, timeout=self.timeout)
            self._session.close()
            self._session.cookies.clear()
            self._logged = False
            # set license to Valid by default to ensure rechecked at login

            self.logging(res)

            return True
        except Exception as e:
            self.logging(e)
            return False

    @staticmethod
    def logging(response):
        try:
            LOG.debug("response content type : %s", response.headers['content-type'])
            LOG.debug("Request : %s on url : %s  ", response.request.method,
                      response.request.url)
            LOG.debug("Response : http code %s  reason : %s  ",
                      response.status_code, response.reason)
            LOG.debug("raw response:  %s ", response.content)
        except:
            LOG.warning("method errors in request when global")

    def update_cookie(self):
        # Retrieve server csrf and update session's headers
        LOG.debug("cookies are  : %s ", self._session.cookies)
        for cookie in self._session.cookies:
            if cookie.name == 'ccsrftoken':
                csrftoken = cookie.value[1:-1]  # token stored as a list
                LOG.debug("csrftoken before update  : %s ", csrftoken)
                self._session.headers.update({'X-CSRFTOKEN': csrftoken})
                LOG.debug("csrftoken after update  : %s ", csrftoken)
        LOG.debug("New session header is: %s", self._session.headers)

    def format_url(self, path):
        return self.url_prefix + path

    def get(self, path):

        url = self.format_url(path)

        return self._session.get(url)

    def post(self, path, para):

        url = self.format_url(path)

        return self._session.post(url, json.dumps(para))

    def delete(self, path):
        url = self.format_url(path)

        return self._session.delete(url)

    def put(self, path, para):
        url = self.format_url(path)

        return self._session.put(url, json.dumps(para))

    def _render(self, template, **message):
        '''Render API message from it's template

                :param template: defined API message with essential params.
                :param message: It is a dictionary, included values of the params
                                for the template
                '''
        if not message:
            message = {}
        msg = jinja2.Template(template).render(**message)
        return json.loads(msg)

    def send_req(self, template, **message):

        template_data = self._render(template, **message)
        path = template_data["path"]
        method = template_data["method"]

        if method == "GET":
            return self.get(path)
        elif method == "POST":
            para = template_data["body"]["json"]
            return self.post(path, para)
        elif method == "PUT":
            para = template_data["body"]["json"]
            return self.put(path, para)

        elif method == "DELETE":
            return self.delete(path)

        else:
            raise Exception("method not support ")



     # QOS

    def add_traffic_shaper(self, **message):
        return self.send_req(ADD_TRAFFIC_SHAPERS,
                             **message
                             )

    def set_traffic_shaper(self, **message):
        return self.send_req(SET_TRAFFIC_SHAPERS,
                             **message
                             )

    def del_traffic_shaper(self, **message):
        return self.send_req(DELETE_TRAFFIC_SHAPERS,
                             **message
                             )

    def get_traffic_shaper(self, **message):
        return self.send_req(GET_TRAFFIC_SHAPERS,
                             **message
                             )

    def add_traffic_policy(self, **message):
        return self.send_req(ADD_TRAFFIC_POLICY,
                             **message
                             )

    def set_traffic_policy(self, **message):
        return self.send_req(SET_TRAFFIC_POLICY,
                             **message
                             )

    def del_traffic_policy(self, **message):
        return self.send_req(DELETE_TRAFFIC_POLICY,
                             **message
                             )

    def get_traffic_policy(self, **message):
        return self.send_req(GET_TRAFFIC_POLICY,
                             **message
                             )


    # VPN

    def add_vpn_p1(self, **message):
        return self.send_req(ADD_VPN_P1,
                             **message
                             )

    def set_vpn_p1(self, **message):
        return self.send_req(SET_VPN_P1,
                             **message
                             )

    def del_vpn_p1(self, **message):
        return self.send_req(DELETE_VPN_P1,
                             **message
                             )

    def get_vpn_p1(self, **message):
        return self.send_req(GET_VPN_P1,
                             **message
                             )

    def add_vpn_p2(self, **message):
        return self.send_req(ADD_VPN_P2,
                             **message
                             )

    def set_vpn_p2(self, **message):
        return self.send_req(SET_VPN_P2,
                             **message
                             )

    def del_vpn_p2(self, **message):
        return self.send_req(DELETE_VPN_P2,
                             **message
                             )

    def get_vpn_p2(self, **message):
        return self.send_req(GET_VPN_P2,
                             **message
                             )

    def add_route_static(self, **message):
        return self.send_req(ADD_ROUTER_STATIC,
                             **message
                             )

    def set_route_static(self, **message):
        return self.send_req(SET_ROUTER_STATIC,
                             **message
                             )

    def del_route_static(self, **message):
        return self.send_req(DELETE_ROUTER_STATIC,
                             **message
                             )

    def get_route_static(self, **message):
        return self.send_req(GET_ROUTER_STATIC,
                             **message
                             )

    # Address
    def get_address(self, **message):
        return self.send_req(GET_FIREWALL_ADDRESS,
                             **message)

    def set_address(self, **message):
        return self.send_req(SET_FIREWALL_ADDRESS,
                             **message)

    def add_address(self, **message):
        return self.send_req(ADD_FIREWALL_ADDRESS,
                             **message)

    def del_address(self, **message):
        return self.send_req(DELETE_FIREWALL_ADDRESS,
                             **message)

    def get_address_group(self, **message):
        return self.send_req(GET_FIREWALL_ADDRGRP,
                             **message)
    # Address Group

    def add_address_group(self, **message):
        return self.send_req(ADD_FIREWALL_ADDRGRP,
                             **message)

    def set_address_group(self, **message):
        return self.send_req(SET_FIREWALL_ADDRGRP,
                             **message)

    def del_address_group(self, **message):
        return self.send_req(DELETE_FIREWALL_ADDRGRP,
                             **message)

    # Service
    def get_service(self, **message):
        return self.send_req(GET_FIREWALL_SERVICE,
                             **message)
    # Service_Group
    def get_service_group(self, **message):
        return self.send_req(GET_FIREWALL_SERVICE_GROUP,
                             **message)

    # NAT

    def add_vip(self, **message):
        return self.send_req(ADD_FIREWALL_VIP,
                             **message
                             )


    def del_vip(self, **message):
        return self.send_req(DELETE_FIREWALL_VIP,
                             **message
                             )

    def get_vip(self, **message):
        return self.send_req(GET_FIREWALL_VIP,
                             **message
                             )

    def add_ippool(self, **message):
        return self.send_req(ADD_FIREWALL_IPPOOL
                             **message
                             )


    def del_ippool(self, **message):
        return self.send_req(DELETE_FIREWALL_IPPOOL,
                             **message
                             )

    def get_ippool(self, **message):
        return self.send_req(GET_FIREWALL_IPPOOL,
                             **message
                             )

    def add_cent_nat(self, **message):
        return self.send_req(add_central_snat_map,
                             **message
                             )

    def get_cent_nat(self, **message):
        return self.send_req(get_central_snat_map,
                             **message
                             )

    def del_cent_nat(self, **message):
        return self.send_req(del_central_snat_map,
                             **message
                             )

    def set_cent_nat(self, **message):
        return self.send_req(set_central_snat_map,
                             **message
                             )

    # Int

    def get_int(self, **message):
        return self.send_req(GET_INTERFACE,
                             **message
                             )

    def set_int(self, **message):
        return self.send_req(SET_INTERFACE,
                             **message
                             )

    def add_int(self, **message):
        return self.send_req(ADD_INTERFACE,
                             **message
                             )

    def del_int(self, **message):
        return self.send_req(DELETE_INTERFACE,
                             **message
                             )
    # Vdom

    def get_vdom(self, **message):
        return self.send_req(GET_VDOM,
                             **message
                             )

    def add_vdom(self, **message):
        return self.send_req(ADD_VDOM,
                             **message
                             )

    def del_vdom(self, **message):
        return self.send_req(DELETE_VDOM,
                             **message
                             )


    # Policy
    def add_firewall_policy(self, **message):
        return self.send_req(ADD_FIREWALL_POLICY,
                             **message
                             )

    def get_firewall_policy(self, **message):
        return self.send_req(GET_FIREWALL_POLICY,
                             **message
                             )

    def set_firewall_policy(self, **message):
        return self.send_req(SET_FIREWALL_POLICY,
                             **message
                             )

    def del_firewall_policy(self, **message):
        return self.send_req(DELETE_FIREWALL_POLICY,
                             **message
                             )

    # Monitor
    def get_system_userange(self, **message):
        return self.send_req(GET_SYSTEM_UseRange,
                             **message
                             )

    def get_ha_status(self, **message):
        return self.send_req(GET_HA_STATIUS,
                             **message
                             )

    def get_inteface_status(self, **message):
        return self.send_req(GET_Interface_Status,
                             **message
                             )

    def get_ipsec_status(self, **message):
        return self.send_req(GET_IPSEC_STATIUS,
                             **message
                             )

    def get_routeing_table(self,**message):
        return self.send_req(GET_ROUTING_TABLE,
                             **message
                             )

    def get_bandwidtg_used(self,**message):
        return self.send_req(GET_Bandwidth_USED,
                             **message
                             )

    def get_ssl_settings(self, **message):
        return self.send_req(GET_VPN_SSL_Settings,
                             **message
                             )

    def put_ssl_settings(self, **message):
        return self.send_req(PUT_VPN_SSL_Settings,
                             **message
                             )

    def add_ssl_policy(self, **message):
        return self.send_req(ADD_VPN_SSL_Policy,
                             **message
                             )

    def get_ssl_policy(self, **message):
        return self.send_req(GET_VPN_SSL_Policy,
                             **message
                             )

    def put_ssl_policy(self, **message):
        return self.send_req(PUT_VPN_SSL_Policy,
                             **message
                             )

    def del_ssl_policy(self, **message):
        return self.send_req(DEL_VPN_SSL_Policy,
                             **message
                             )

    def add_user(self, **message):
        return self.send_req(ADD_LOCAl_USER,
                             **message
                             )

    def del_user(self, **message):
        return self.send_req(DEL_LOCAl_USER,
                             **message
                             )

    def put_user(self, **message):
        return self.send_req(PUT_LOCAl_USER,
                             **message
                             )

    def get_user(self, **message):
        return self.send_req(GET_LOCAl_USER,
                             **message
                             )

    def add_user_group(self,**message):
        return self.send_req(ADD_USER_GROUP,
                             **message
                             )

    def del_user_group(self,**message):
        return self.send_req(DEL_USER_GROUP,
                             **message
                             )

    def put_user_group(self,**message):
        return self.send_req(PUT_USER_GROUP,
                             **message
                             )

    def get_user_group(self,**message):
        return self.send_req(GET_USER_GROUP,
                             **message
                             )

