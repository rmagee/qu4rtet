.. image:: https://github.com/rmagee/qu4rtet/actions/workflows/django.yml/badge.svg
    :target: https://github.com/rmagee/qu4rtet/actions/workflows/django.yml

I am the original developer of the QU4RTET system.  This is my personal repo for both advancing and maintainig the open source project going forward.

QU4RTET: The Open-Source EPCIS / Level-4
========================================

.. code-block:: text

    MWNNNWWWNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNWNWWMMMMMMMMMMMMMMMMMMMWWNNNNNNWWM
    WXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0KWMMMMMMMMMMMMMMMMMMMN0OOOOOO0NM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxk0NMMMMMMMMMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxOXWMMMMMMMMMMMMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxkOKXWMMMMMMMMMMMMMMMMMMMMMMMMXOxxxxxxOXW
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxk0NWMMMMMMMMMMMMMMMMMMMMMMMMMMXOxxxxxxOXW
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxk0NMMMMMMMMMMMMMWWMMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKNMMMMMMMMMMMMMNKXWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMWN0kKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxOXWMMMMMMMMMMMMWXOxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxkOXWMMMMMMMMMMMMWKkxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxOXWMMMMMMMMMMMMN0kxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxk0NMMMMMMMMMMMMWN0kxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxk0NMMMMMMMMMMMMWXOxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMWKkxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMN0kxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxxOXWMMMMMMMMMMWNKOkxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxxxOXWMMMMMMMMMMWXOkxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxxk0NMMMMMMMMMMMWKkxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxxk0NMMMMMMMMMMMN0kxxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxxxxxxxxxxxxkKNMMMMMMMMMMMWK000OO00O000000000XMMMMMMMMMMMMMN00O00000NM
    WKkxxxxxxxxxxxxxkKWMMMMMMMMMMMMMWWWWWWWWWWWWWWWWWWMMMMMMMMMMMMMMMWWWWWWWWMM
    WKkxxxxxxxxxxxxOXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    WKkxxxxxxxxxxxOXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    WKkxxxxxxxxxkOXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    WKkxxxxxxxxk0NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    WKkxxxxxxxk0NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    WKkxxxxxxk0XNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNWMMMMMMMMMMMMMWNNNNNNNNWM
    WKkxxxxxxxkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkOXWMMMMMMMMMMMMXOkkkkkkOXM
    WKkxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxxxO0KKK0KKKKKK00OkxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkxk0NWMMMMMMMMMMWN0kxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKkk0NMMMMMMMMMMMWN0kxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WKOKNMMMMMMMMMMMWXOxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxkKWMMMMMMMMMMMMXOxxxxxxOXM
    WXXWMMMMMMMMMMMWX0kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkOXWMMMMMMMMMMMMXOkkkkkkOXM
    MWWMMMMMMMMMMMMWNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXNMMMMMMMMMMMMMWNXXXXXXNWM


The open-source EPCIS / level-4 system.

:License: GPLv3

Getting Started
---------------

There are a few ways to get started quickly with QU4RTET, the fastest of
which is via the docker-compose file `local.yml` in the root directory.  For
more info on getting the docker-compose and other environments set up, check
out the documentation here:

https://serial-lab.gitlab.io/qu4rtet/

Features
--------

QU4RTET-UI
++++++++++
The QU4RTET-UI is a graphical interface to manage multiple QU4RTET systems.
Manage all of your systems, test, qa, development, production, etc. inside of
one interface.  You can find the quartet-ui here:

https://gitlab.com/serial-lab/quartet-ui/


Docker Compose Builds
+++++++++++++++++++++
The root directory contains a docker-compose build that works right out
of the box and is the easiest way to get going.  For more see the documentation.


VirtualBox Image
++++++++++++++++
** Note: the virtualbox image is not part of our automated build.  It is
usually somewhat up to date but you will want to follow the update instructions
in the documentation here under the virtualbox page:

https://serial-lab.gitlab.io/qu4rtet/

There is a virtualbox image that is available at bintray.com- see the link
here:



OpenAPI Specification Support (Swagger)
+++++++++++++++++++++++++++++++++++++++
All of the APIs exposed by QU4RTET are available via an *OpenAPI* schema.
This allows you to quickly browse the API and also generate client SDKs in
over 40 languages.  For more, see:

https://www.openapis.org/

EPCIS Support
+++++++++++++
QU4RTET supports the current EPCIS 1.2 XML format.  All inbound messages,
considering that EPCIS 1.2 is backwards compatible, that are compliant with
the GS1 schemas for EPCIS 1.0.1, 1.1 and 1.2 will parse correctly.  GS1 USHC
is not supported at this time.

For more on EPCIS 1.2:
https://www.gs1.org/standards/epcis


Distributed Task Processing
+++++++++++++++++++++++++++
QU4RTET handles all parsing and processing via the *Celery Distributed Task
Queue*.  This allows work and processing to be spread out amongst any number
of virtual machines, containers, physical servers, etc.  This allows for a
myriad of flexible scalability-oriented architectures.

For more:

http://www.celeryproject.org/

Built In Extensibility
++++++++++++++++++++++
The `quartet_capture` component is the foundation for the internal QU4RTET
rule engine that handles inbound (and will handle outbound) message parsing by
inheriting from a simple class and imlementing a simple function call.
For example, the code below is how the `qu4rtet_epcis` package exposes EPCIS
parsing to the rule engine:

.. code-block:: python

    import io
    from quartet_capture.rules import Step
    from quartet_epcis.parsing.parser import QuartetParser
    from django.core.files.base import File

    class EPCISParsingStep(Step):
        '''
        Calls the EPCIS parser as a rules.Step that can be used in the
        quartet_capture rule engine.
        '''
        def declared_parameters(self):
            return {}

        def execute(self, data, rule_context: dict):
            try:
                if isinstance(data, File):
                    parser = QuartetParser(data)
                else:
                    parser = QuartetParser(io.BytesIO(data))
            except TypeError:
                parser = QuartetParser(io.BytesIO(data.encode()))
            parser.parse()

Opbeat Integration
++++++++++++++++++
Want to monitor the performance of your QU4RTET instance in real time?
QU4RTET comes ready with Opbeat support.  Sign up for an opbeat account and
add the account credentials to your configuration and you're ready to go.  More is available in the
installation documentation in the project docs.

More: https://opbeat.com/

Sentry Integration
++++++++++++++++++
Want a central online mechanism to monitory your QU4RTET logs?  Want to have
real-time alerts let your team know if anything is wrong with your instance?
QU4RTET comes ready with Sentry configuration options.  Sign up for an account
and add your configurations and you're done.  More is available in the
installation documentation in the project docs.

More: https://sentry.io/



