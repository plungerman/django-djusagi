# -*- coding: utf-8 -*-

import sys

from djusagi.groups.manager import GroupManager


def main():
    """Fetch and display all of the google groups from a given domain."""
    # group settings manager
    gm = GroupManager()
    # retrieve all groups in the domain
    group_list = gm.groups_list()
    # cycle through the groups
    for group in group_list:
        #g = gm.groups_get(group['email'])
        #print(g)
        #print(group)
        # fetch the group settings
        g = gm.group_settings(group['email'])
        #print(g)
        #print(g['whoCanViewGroup'])
        # fetch the group members
        #members = gm.group_members(group['email'])
        # fetch the group owner
        #owner = gm.group_owner(members)
        #if owner:
            #owner = owner['email']
        # dump
        #print(group)
        #print('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(
            #group['name'], owner, g['email'], g['whoCanJoin'],
            #g['whoCanViewGroup'] , g['whoCanViewMembership'],
            #g['whoCanPostMessage'], g['membersCanPostAsTheGroup'],
            #g['whoCanContactOwner'], g['whoCanInvite']
        #))


if __name__ == '__main__':
    sys.exit(main())
