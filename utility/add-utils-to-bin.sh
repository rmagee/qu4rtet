#!/usr/bin/env bash
echo "Adding QU4RTET commands to the system path"
chmod ag+x -R /srv/qu4rtet/utility/*.sh
ln -s /srv/qu4rtet/utility/restart-quartet.sh /usr/local/bin/restart-quartet
ln -s /srv/qu4rtet/utility/restart-quartet.sh /usr/local/bin/stop-quartet
ln -s /srv/qu4rtet/utility/restart-quartet.sh /usr/local/bin/update-quartet
echo "Complete."
