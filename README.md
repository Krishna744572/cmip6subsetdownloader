# NEX-GDDP-CMIP6 Subset Builder

A simple web tool that builds a ready to run Python downloader for the NASA NEX-GDDP-CMIP6 daily climate projections. Instead of downloading global files of about 220 MB per year, you download only your study area, so a full download needs megabytes rather than hundreds of GB.

**Live tool:** https://krishna744572.github.io/cmip6subsetdownloader/

## What it does

* Lets you choose a CMIP6 model, scenarios (historical, SSP126, SSP245, SSP370, SSP585), variables (pr, tasmin, tasmax, tas, sfcWind, rsds, rlds, huss, hurs) and a year range.
* Lets you enter a bounding box (south, north, west, east) in decimal degrees.
* Generates a Python script and a plain URL list that use the NASA THREDDS NetcdfSubset service.
* Downloads happen on your own computer. This page does not store or transfer any climate data.

## How to use

1. Open the live tool and fill in your choices.
2. Click **Build my downloader**.
3. Copy the Python script, save it as `download.py`, install the requests package (`pip install requests`), and run `python download.py`.
4. Alternatively, copy the URL list into a download manager, for example `aria2c -i urls.txt`.

Tips: the grid is 0.25 degrees, so add a small margin around your basin. Test one year first before starting a long download.

## Standalone script

The file `cmip6_subset_downloader.py` is an interactive command line version of the same downloader, with resume safe checks and retries.

## Data source and citation

Data: NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6), prepared by NASA Earth Exchange and the Climate Analytics Group and distributed by the NASA Center for Climate Simulation (NCCS). This repository contains no data. It only contains code that requests subsets from NASA's public server.

Please follow the dataset's terms of use (the underlying CMIP6 model outputs carry their own licenses) and cite:

Thrasher, B., Wang, W., Michaelis, A., Melton, F., Lee, T., and Nemani, R. (2022). NASA Global Daily Downscaled Projections, CMIP6. Scientific Data, 9, 262. https://doi.org/10.1038/s41597-022-01393-4

## Disclaimer

This is an unofficial tool provided as is, without warranty. It is not affiliated with or endorsed by NASA or the CMIP6 modeling groups. Users are responsible for checking the data terms and validating results for their own use.
