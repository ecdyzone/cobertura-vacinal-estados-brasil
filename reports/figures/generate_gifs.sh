#!/bin/bash

# apt install imagemagick

convert -delay 200 -loop 0 swarmplots/*.png swarmplot_2017_2020.gif

convert -delay 300 -loop 0 cloropleths/*.png cloropleth_2017_2020.gif


