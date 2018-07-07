## FAQ/Troubleshooting ##
{:.no_toc}

* TOC
{:toc}

{::options coderay_line_numbers="nil" /}



### What if my computer doesn't meet requirements? ### 
{:#camb-legacy}
Cosmology@Home runs multiple "apps." The [requirements list](join.php#requirements) is for the default app (named *camb_boinc2docker*), but if your computer does not meet them, there is an older app available (named *camb_legacy*) which runs on just Windows and Linux but supports 32-bit processors and does not need Virtualbox or VT-x/AMD-v. At this point we only use the results from *camb_legacy* for testing the [PICO](#science) algorithm and not for comparing with data since the app is fairly old. However, the results do serve a limited purpose and allow Cosmology@Home users who do not meet the above requirements to continue to contribute, thus we continue to provide it. We encourage users who can run *camb_boinc2docker* to do so, however. 

### What is VT-x or AMD-v and why do I need it? ###
{:#vtx}
This is a feature of modern processors which provides hardware support for virtualization (Intel calls theirs "VT-x" and AMD calls theirs "AMD-v"). 

The default Cosmology@Home apps are 64bit virtual machines, and to run these virtual machines Virtualbox needs your CPU to support VT-x/AMD-v and this feature has to be *enabled* (it often comes disabled by default with new computers). 

After the first time your computer connects to the Cosmology@Home server to request a job, you will be able to see on the "Computer information" page information about your CPU's virtualization support (visit [this page](https://www.cosmologyathome.org/hosts_user.php) while logged in and click "Details" for the computer you are interested in). 

If under virtualization you see "None", it means you need to install Virtualbox. If you see that your CPU does not support hardware virtualization, unfortunately this computer cannot run the default Cosmology@Home apps. If you see that it does have support but it is disabled, then you need to reboot your computer, enter your BIOS, find this option and enable it. Here is an example of what it might look like (although this will vary with BIOS version, it will likely say something about virtualization): 

![test](img/vtx.png)


### I enabled VT-x/AMD-v but I still don't receive jobs ###

Sometimes the client can get stuck in a state where it still thinks this feature is disabled despite that you have enabled it. This can happen sometimes if you attempted to run a *camb_boinc2docker* job before enabling VT-x/AMD-v, it may also be accompanied by a message "Scheduler wait: Please upgrade BOINC to the latest version" and the log files may show "ERROR: Invalid configuration. VM type requires acceleration but the current configuration cannot support it." To fix this:

* Remove the Cosmology@Home project
* Shut down the BOINC client (from Advanced View choose the menu option *Advanced->Shutdown Connected Client*)
* Go to your BOINC folder and edit the file `client_state.xml`
* Remove the line which contains `<p_vm_extensions_disabled>`
* Restart your BOINC client and readd the project

### My computer gets very slow while Cosmology@Home is running in the background ###

Some users prefer to have Cosmology@Home running at all times in the background, even while they're using their computer. Unfortunately, due to a [regression](https://www.virtualbox.org/ticket/13500) in VirtualBox, on Windows the priority of VirtualBox cannot be set to low, so it may interfere with your usage. As a workaround until VirtualBox is fixed, you can either lower your BOINC global CPU usage, or you can [limit](#limit-cpu) the number of CPUs that Cosmology@Home uses (leaving your other CPUs for native BOINC applications from other projects which *can* be set to low priority). 



### How can I limit the number of CPUs used? ###
{:#limit-cpu}

*camb_boinc2docker* is multi-threaded and will use up all available cores which BOINC allows it to. For example, if in the BOINC computing preferences you have set "Use at most 50% CPU time" and you have a 4-core processor, the job will use two of them. 

If for whatever reason you wish to limit the number of cores used without changing the global BOINC CPU usage, you can do so by creating a file called `"app_config.xml"` in the Cosmology@Home project folder and adding the following text, with the "2" under `avg_ncpus` replaced by however many CPUs you want to use (thanks to [Crystal Pellet](http://www.cosmologyathome.org/forum_thread.php?id=7227&nowrap=true#20300)):

~~~xml
<app_config>
    <app>
        <name>camb_boinc2docker</name>
        <max_concurrent>1</max_concurrent>
    </app>
    <app_version>
        <app_name>camb_boinc2docker</app_name>
        <plan_class>vbox64_mt</plan_class>
        <avg_ncpus>2</avg_ncpus>
    </app_version>
</app_config>
~~~

*Notes:* 

* If after this BOINC gives an error reading your `app_config.xml` file, make sure you saved the file with a character encoding apropriate for your system (options to do so may vary by text editor).
* You will need to restart your BOINC client for this take effect
* This will only affect jobs started after you created the file (jobs started before will show "X CPUs" but still run using all of them, you can just abort these) 
* Reseting or removing/readding the project will delete this file so you will have to remake it

### What science is being done with Cosmology@Home? ###
{:#science}
For an introduction to the science we do at Cosmology@Home, see [this](http://cosmicmar.com/posts/tbd) (link will be posted shortly) multi-part blog post. 

To summarize, we run the [CAMB](http://camb.info) code, the results from which are used to train the [PICO](https://sites.google.com/a/ucdavis.edu/pico/) code, which in turn is used by various groups in the field to analyze cosmological datasets. Most notably, PICO is used extensively in the analysis of [Planck](http://www.esa.int/Our_Activities/Space_Science/Planck) data (e.g. this [paper](http://xxx.lanl.gov/abs/1507.02704)). The papers describing PICO itself can be found [here](http://arxiv.org/abs/astro-ph/0606709) and [here](http://arxiv.org/abs/0712.0194) (click "PDF" on the right to view the papers for free). Citations to these papers can be found [here](http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=2007ApJ...654....2F&amp;refs=CITATIONS&amp;db_key=AST) and [here](http://adsabs.harvard.edu/cgi-bin/nph-ref_query?bibcode=2007arXiv0712.0194F&amp;refs=CITATIONS&amp;db_key=PRE) and represent work which has referenced PICO and hence benefited from Cosmology@Home in some way. 

### How do I only run the legacy application? ###

If you wish to use only the old Cosmology@Home application, *camb_legacy*, you can edit your [preferences](http://www.cosmologyathome.org/prefs.php?subset=project) and unselect all other applications. The results from this application are not as useful so please consider doing so only if you are having technical problems running the other applications. Note *camb_legacy* only supports Windows and Linux.  



### How does the *camb_boinc2docker* app work? ###

The *camb_boinc2docker* jobs (or any other Cosmology@Home jobs relying on *boinc2docker*) run a [Virtualbox](https://en.wikipedia.org/wiki/VirtualBox) "virtual machine" on your computer, inside of which we run a [Docker](https://www.docker.com/whatisdocker) "container" which packages the science application. This nesting of Docker inside of Virtualbox might seem redundant, but is quite powerful. The use of Virtualbox means our applications will always work on Mac OSX, Windows, and Linux. The use of Docker means we can keep our Virtual machine images extremely small (only a few tens of MB), and when updates are needed, your computer will only need to re-download the Docker "layers" which actually changed. 

### What is *boinc2docker*? ###
This is the name for the software which allows us to run Docker containers with BOINC. It can be used to run any code, *camb_boinc2docker* being one of them. You can follow development of boinc2docker or use it with your own project here: [https://github.com/marius311/boinc2docker](https://github.com/marius311/boinc2docker). 

### Why is there no 32-bit support? ###
Docker only supports 64-bit processors. For those with 32-bit computers wishing to contribute to Cosmology@Home, you might still be able to run the [legacy application](#camb-legacy). 


### Can I see the source code of Cosmology@Home? ###
Absolutely! All of the code, including the *camb_boinc2docker* code itself as well as the server code is publicly available on the [github page](https://github.com/marius311/cosmohome). In fact, the *exact* commit the server is currently running can be seen on the [server status](server_status.php) page. We run our server from a Docker container, so its super easy for anyone run a copy of our server too, and play around with modifying or seeing how it works. 


### Does it hinder Cosmology@Home if I abort jobs? ###
No, feel free to abort jobs if you need to. Our results are built up by the aggregate of all jobs, and losing any one particular result is fine. 
