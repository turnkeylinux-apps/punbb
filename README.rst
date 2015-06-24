PunBB - Forum software
======================

`PunBB`_ is a fast and lightweight PHP-powered discussion board.  Its
primary goals are to be faster, smaller and less graphically intensive
as compared to other discussion boards. PunBB has fewer features than
many other discussion boards, but is generally faster and outputs
smaller, semantically correct XHTML-compliant pages.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- PunBB configurations:
   
   - Installed from upstream source code to /var/www/punbb

- SSL support out of the box.
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, phpMyAdmin: username **root**
-  PunBB: username **admin**


.. _PunBB: http://punbb.informer.com/
.. _TurnKey Core: http://www.turnkeylinux.org/core
.. _Adminer: http://www.adminer.org/
