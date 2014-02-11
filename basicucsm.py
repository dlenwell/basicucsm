#!/usr/bin/python

# Copyright (c) 2014 David Lenwell - Piston Cloud Computing, Inc. , All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
from pyucsm import *


class ComputeObject(object):
    """ ucsm compute object .. represents a server essentially 
    attaching common attributes to properties and power control functions"""

    nics = {}
    boot_nic = None

    # possible power states
    power_states = ["up",
                    "down",
                    "soft-shut-down",
                    "cycle-immediate",
                    "hard-reset-immediate",
                    "bmc-reset-immediate",
                    "bmc-reset-default",
                    "cmos-reset-immediate",
                    "diagnostic-interrupt"]

    def __init__(self, c, node):
        """does some ugly recursion to pull the nic info out of the xml"""
        self.name = node.attributes['assignedToDn']
        
        # find the nics.. NOTE: this is hacky.. 
        #   need to switch to using the search function 
        for child in node.children:
            if child.ucs_class == 'adaptorUnit':
                for nic in child.children:
                    if nic.ucs_class == 'adaptorHostEthIf':
                        self.nics[nic.attributes['name']] = nic.attributes
                        if nic.attributes['bootDev'] == 'enabled':
                            self.boot_nic = nic.attributes['name']
        
        self._power = None #node.attributes['power']
        self.attributes = node.attributes
        self.c = c 


    @property
    def power(self):
        """ """
        return self._power


    def set_boot(self, options = {}):
        """TODO: sets correct boot priority"""


    def start(self):
        """starts specified server"""
        return self.change_power_state('up')


    def stop(self):
        """changes power state of provided _dn to down.. 
        essentially a forced shutdown"""
        return self.change_power_state('soft-shut-down')


    def reboot(self):
        """"""
        return self.change_power_state('bmc-reset-immediate')


    def hard_reboot(self):
        """ """
        return self.change_power_state('hard-reset-immediate')


    def change_power_state(self, state):
        """ since all the power state changes are the same query with a 
        different state this function handles all of them"""
        # build the xml
        src = UcsmObject()
        src.ucs_class = "pair"
        src.attributes['key'] = "%s/power" % self.name

        lspower = UcsmObject()
        lspower.ucs_class = "lsPower"
        lspower.attributes['dn'] = "%s/power" % self.name
        lspower.attributes['state'] = state
        lspower.attributes['status'] = "modified"
        src.children.append(lspower)

        in_configs_node = minidom.Element('inConfigs')
        in_configs_node.appendChild(src.xml_node(True))

        print in_configs_node.toprettyxml()

        data, conn = self.c._perform_query('configConfMos',
                                             data=in_configs_node,
                                             cookie=self.c.cookie,
                                             inHierarchical="yes")

        #self.c._check_is_error(data.firstChild)     dn="%s/power" % _dn,
        #res = self.c._get_single_object_from_response(data)
        return data.toprettyxml() 


class BasicUcsm(UcsmConnection):
    """ just a wrapper to make ucs more sane to deal with """
    # dict of nodes 
    nodes = {}

    def __del__(self):
        """ logs the user out because the object is finished """
        self.logout()


    def __init__(self, host ,username, password, port=None, secure=False, *args, **kwargs):
        """ supers original init then logs the user into the server and 
        populates the nodes dict"""
        #construct 
        super(BasicUcsm,self).__init__(host, port, secure, *args, **kwargs)

        # login 
        self.cookie = self.login(username, password)

        # populate compute dict
        self._populate_list()


    def _populate_list(self):
        """ populates a local python dictionary object of servers"""
        nodes = self.resolve_class('computeItem', hierarchy=True)

        for node in nodes:
            if node.attributes.has_key('assignedToDn') and node.attributes['assignedToDn'] != '':
                self.nodes[node.attributes['assignedToDn']] = ComputeObject(self, node)


    def _print_list(self):
        """prints the list.. just for debugging """
        for k,v in self.nodes.iteritems():
            print k,v


    