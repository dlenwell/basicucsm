#!/usr/bin/python

# Copyright (c) 2014 David Lenwell, Piston Cloud Computing, Inc. , All Rights Reserved
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

"""
    demo script for BasicUcsm 
"""
from basicucsm import * 


""" 
auth and host values

I had to create a user who was not the admin and assign it 
the correct rolls. This way 
"""
username = "grandpa"
password = "MonkeyBalls01"
host = "172.16.200.134"


"""
When instantiated basicucsm  logs in to the ucsm api .. runs some queries
builds a local dict of compute node objects

"""
ucsm_thing = BasicUcsm(host, username, password)







"""
the pyucsm object persists a connection .. so if you don't logout when 
your finished it leaves a ghost session logged in and you'll reach the 
maximum allowed sessions and things will be inaccessible.

"""
ucsm_thing.logout()


"""
Because you have to assign a service profile to a server before you can 
control its power state I've hard coded one of the service profiles with
the name "org-root/ls-rack-unit"

lets try to hard reboot it and see what happens. 



"""
print ucsm_thing.nodes["org-root/ls-rack-unit"].start()

