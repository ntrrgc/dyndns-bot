#DynDNS bot

Starting from 13 of May of 2013, DynDNS started requiring its free user to log
in DynDNS portal every 30 days in order to maintain their accounts or switch to
DynDNS Pro (using ddclient is not sufficient).

Of course, this a big nuisance for free users, who surely have better things to
remember than the last time they log in DynDNS portal.

So this is a little script for Linux that logs in your DynDNS account
invisibly. You can set it in cron (daily, weekly or as you wish).

In case anything fails, it will return non-zero and print the traceback both
through stderr and syslog.

Every time it logs in it saves a screenshot in a directory you specify, so you
can check the bot is working properly.

#Requirements

 * python-selenium
 * PyVirtualDisplay
 * xorg-server-xvfb
 * xorg-server-xephyr (optional, only if you want to see how DynDNS bot is
   running)

#How to install

Install xorg-server-xvfb and xorg-server-xephyr (this last is optional) from
your distro packages.

Install a python virtualenv within that directory and activate it:

    virtualenv env
    source env/bin/activate

(ArchLinux users must use virtualenv2 instead of virtualenv)

Use pip to install Selenium and PyVirtualDisplay.

    pip install Selenium PyVirtualDisplay

Installation done!

Now you have to set up a configuration file on `~/.config/dyndns.json` like
this:

    {
       "username": "foo",
       "password": "bar",
       "screenshots_path": "~/dyndns"
    }

Run the script with the following command.

    python dyndns.py -v

**Note:** `-v` tells the bot to show you his screen. In order to use it you
need to have Xephyr installed.

Everything is ok? Now remove the `-v` and check you still get no error (no
output) and a screenshot has been created on the path you wrote in your
settings.

#One line command to run the bot

Replace `<PATH>` with the full path you installed the bot into.

    <PATH>/env/bin/python <PATH>/dyndns.py

#Add it to cron

Make sure you have cron installed (in whatever flavour) and running.

In case you use an *anacron-like* flavour of cron (i.e. *cronie*) you may have
a directory like `/etc/crond.daily`. Use it to store a cron script. Here is an
example:

    #!/bin/bash
    sleep 5m # Don't make boot slower
    exec su - <USER> -c '<PATH>/env/bin/python <PATH>/dyndns.py'

Substitute `<PATH>` with the path you installed DynDNS bot into and `<USER>`
with the user you want it to run as (normally, your username). Save it as
`/etc/cron.daily/dyndns-bot` and give it execution permission with `chmod u+x
/etc/cron.daily/dyndns-bot`.
