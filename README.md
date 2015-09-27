# ec2-power - scheduled shutdown/startup of ec2/euca instances

Manage instances power state with tags based on cron time formats.

-   ec2-power.sh is an example cloud-init setup
-   ec2-power.py is the script ran from cron

tags used are:

-   auto:start  : "0 10 \* \* \*" - will start instance at 10am daily
-   auto:stop   : "0 20 \* \* \*" - will halt instance at 8pm daily
-   auto:ignore : (null) - host will be ignored from stop schedule until tag
    is removed

note all times should be UTC as thats what AWS uses.

the script will ignore any host that does not have:

-   disableApiTermination = True
-   instanceInitiatedShutdownBehaviour = stop

any host with an auto:ignore tag key (no value required) will not be stopped
but will still be started if required.

debug mode is enabled, cron job is disabled by default.

an appropriate IAM profile needs to be applied to the host running this with
ec2:DescribeInstances, ec2:StartInstances and ec2:StopInstances actions.

credit for this should go to [Shing Chen](http://schen1628.wordpress.com/2014/02/04/auto-start-and-stop-your-ec2-instances/) all I have done is changed output and
added some sanity checking and the ignore tag to it.
