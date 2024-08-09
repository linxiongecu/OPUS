# GPS_OPUS
# step 1 install chrome browser

# step 2 install seleilium 
pip install selenium
# step 3 get sample GPS rinex files
### curl -O https://geodesy.noaa.gov/corsdata/rinex/YYYY/DDD/ssss/ssssDDD0.YYd.gz
### check gnss station name 
https://www.arcgis.com/apps/webappviewer/index.html?id=190385f9aadb4cf1b0dd8759893032db&extent=-30657930.8234%2C-3999003.0107%2C3507586.3314%2C12379311.914%2C102100&showLayers=17bf0a87f3a-layer-16%3B17bf0a87f38-layer-14%3B17bf0a87f36-layer-13
### download data at greenbelt,MD:  gods
curl -O https://geodesy.noaa.gov/corsdata/rinex/2023/100/gods/gods1000.23o.gz

curl -O https://geodesy.noaa.gov/corsdata/rinex/2023/101/gods/gods1010.23o.gz

curl -O https://geodesy.noaa.gov/corsdata/rinex/2023/102/gods/gods1020.23o.gz
### you need to unzip gz file!
# step 4 configure the upload script

# upload GPS files
python OPUS_upload.py
# Read results from Email
ptyhon OPUS_read.py
# files will be saved in GPS.txt
data column will be "Name,Date,Start,End,NAD83_X,NAD83_Y,NAD83_Z,UTM_East,UTM_North,,Ortho,EL,OBS_USED,RMS"
