#!/bin/bash

rm -rf _site
docker run --rm --volume="$PWD:/srv/jekyll" --publish [::1]:4000:4000 jekyll/jekyll jekyll build
rsync -av _site/* barrett1:/afs/cs/group/barrettlab/centaur_www/
