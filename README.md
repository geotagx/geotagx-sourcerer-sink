#GeoTag-X Sourcerer Sink
--------------------------

The GeoTag-X Sourcerer Sink, processes all data collected by numerous GeoTag-X Sourcerers and pushes them into the corresponding GeoTag-X instance as `Tasks` in all the projects associated with the respective category.

TODO:
* Add description of the schema of data points collected by GeoTag-X Sourcerer(s) here

#Installation Instructions
--------------------------

* Add this repository as a submodule in the *root* directory of your GeoTag-X installation.
* Use the `virtualenv` that you use to run GeoTag-X
* Install `GeoTag-X Sourcerer Sink` specific dependencies by running
```bash
pip install -r geotagx_sourcerer_requirements.txt
```
* ```bash
python geotagx_sourcerer_sink.py
```

#Config Parameres
------------------
* `TIME_DELAY` : (seconds) How frequently do you want the GeoTag-X Sourcerer Sink to poll redis for collected images
* DELIMITER : (default : %%%%) The delimiter used by your GeoTag-X instance to separate timestamp from the base64 encoded data
#Author
-------
S.P. Mohanty < sp.mohanty@cern.ch >