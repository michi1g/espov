Import("env")

# Ensure data/ is uploaded to LittleFS when using 'pio run -t uploadfs'
env.Replace(ESP8266FS_DIR="data")
