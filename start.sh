#!/bin/bash
/usr/sbin/apache2ctl -D FOREGROUND;certbot --apache --non-interactive --staging --quiet --agree-tos -d danev.xyz -d www.danev.xyz -m danevd@tcd.ie --no-eff-email
