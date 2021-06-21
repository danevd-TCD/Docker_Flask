#!/bin/bash
/usr/sbin/apache2ctl -D FOREGROUND;certbot --apache --non-interactive --staging --quiet --agree-tos -d csi6220-4-vm1.ucd.ie --no-autorenew -m daniel.danev@ucdconnect.ie --no-eff-email
