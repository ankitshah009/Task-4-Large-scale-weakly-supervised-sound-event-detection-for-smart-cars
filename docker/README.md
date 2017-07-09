Docker containers to reproduce Task4 DCASE2017 Baseline results
=========================================================

This directory contains [docker](https://www.docker.com/) containers to reproduce Task4 DCASE2017 baseline system results. To install Docker Community Edition (Docker CE) follow the instructions from [Docker documentation ](https://docs.docker.com/engine/installation/). 

Use ``Makefile`` to use the provided Docker container. When container is launched first time, Docker will create the container image by downloading and installing the needed libraries (defined in ``Dockerfile``).

For example, to generate the baseline system results for Task 4 run:

    make task4
    
To open bash shell inside the container environment, run:

    make bash

