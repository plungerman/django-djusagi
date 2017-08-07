# -*- coding: utf-8 -*-
import sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from djusagi.groups.manager import GroupManager

def main():
    """
    Fetch and display all of the google groups from a given domain
    """

    # group settings manager
    gm = GroupManager()
    # retrieve all groups in the domain
    group_list = gm.groups_list()
    # cycle through the groups
    for group in group_list:
        # fetch the group settings
        g = gm.group_settings(group["email"])
        # fetch the group members
        members = gm.group_members(group["email"])
        # fetch the group owner
        owner = gm.group_owner(members)
        if owner:
            owner = owner["email"]
        # dump
        print u"{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            group["name"], owner, g["email"], g["whoCanJoin"],
            g["whoCanViewGroup"] , g["whoCanViewMembership"],
            g["whoCanPostMessage"], g["membersCanPostAsTheGroup"],
            g["whoCanContactOwner"], g["whoCanInvite"]
        ).encode("utf-8")

######################
# shell command line
######################

if __name__ == "__main__":

    sys.exit(main())

