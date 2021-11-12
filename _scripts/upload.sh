#!/bin/bash

rm -rf _site
bundle-2.7 exec jekyll build
rsync -av _site/* barrett1:/afs/cs/group/barrettlab/centaur_www/
