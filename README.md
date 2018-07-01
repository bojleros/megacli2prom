# megacli2prom
Megacli to prom textfile exporter. I have created it since my old controller does not report drive details under StorCli.

Example usage (execute from crontab):
> mkdir -m755 /tmp/textcollector >/dev/null 2>&1 ; /usr/local/sbin/megacli.py > /tmp/textcollector/megacli.prom

List of metrics exported on my venerable controller:

```# HELP megacli_pd_info Physical drive detailed info
# TYPE megacli_pd_info gauge
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="disk_group"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="span"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="arm"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="device_id"} 2
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="wwn"} 5764975730775441575
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="sequence_number"} 2
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="size_raw"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="size_non_coerced"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="size_coerced"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="state"} 255
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="port"} 1
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="path"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="ekm_attention_needed"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="0", type="smart_alert"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="disk_group"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="span"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="arm"} 1
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="device_id"} 1
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="wwn"} 5764975730775519087
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="sequence_number"} 2
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="size_raw"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="size_non_coerced"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="size_coerced"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="state"} 255
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="port"} 2
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="path"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="ekm_attention_needed"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="1", type="smart_alert"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="disk_group"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="span"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="arm"} 2
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="device_id"} 3
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="wwn"} 5764975730775513929
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="sequence_number"} 2
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="size_raw"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="size_non_coerced"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="size_coerced"} 2.99946772057e+12
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="state"} 255
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="port"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="path"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="ekm_attention_needed"} 0
megacli_pd_info{adapter="0", enclosure="252", slot="2", type="smart_alert"} 0
# HELP megacli_drives Drives information
# TYPE megacli_drives gauge
megacli_drives{adapter="0", state="Total", type="virtual"} 2
megacli_drives{adapter="0", state="Degraded", type="virtual"} 0
megacli_drives{adapter="0", state="Offline", type="virtual"} 0
megacli_drives{adapter="0", state="PhysicalTotal", type="physical"} 4
megacli_drives{adapter="0", state="DisksTotal", type="physical"} 3
megacli_drives{adapter="0", state="Critical", type="physical"} 0
megacli_drives{adapter="0", state="Failed", type="physical"} 0
# HELP megacli_memory_errors Memory errors
# TYPE megacli_memory_errors gauge
megacli_memory_errors{adapter="0", type="correctable"} 0
megacli_memory_errors{adapter="0", type="uncorrectable"} 0
# HELP megacli_memory_size_bytes Controler memory information
# TYPE megacli_memory_size_bytes gauge
megacli_memory_size_bytes{adapter="0", type="Total memory"} 536870912.0
megacli_memory_size_bytes{adapter="0", type="Write cache"} 362807296.0
# HELP megacli_pd_speed_bits Link and drive speed
# TYPE megacli_pd_speed_bits gauge
megacli_pd_speed_bits{adapter="0", enclosure="252", slot="0", type="drive"} 6442450944.0
megacli_pd_speed_bits{adapter="0", enclosure="252", slot="0", type="link"} 6442450944.0
megacli_pd_speed_bits{adapter="0", enclosure="252", slot="1", type="drive"} 6442450944.0
megacli_pd_speed_bits{adapter="0", enclosure="252", slot="1", type="link"} 6442450944.0
megacli_pd_speed_bits{adapter="0", enclosure="252", slot="2", type="drive"} 6442450944.0
megacli_pd_speed_bits{adapter="0", enclosure="252", slot="2", type="link"} 6442450944.0
# HELP megacli_controller Controler information
# TYPE megacli_controller gauge
megacli_controller{adapter="0", product_name="RAID Ctrl SAS 6G 5/6 512MB (D2616)"} 1
megacli_controller{adapter="0", package_build="12.15.0-0239"} 1
megacli_controller{adapter="0", firmware_version="2.130.403-4660"} 1
megacli_controller{adapter="0", bios_version="3.30.02.2_4.16.08.00_0x06060A05"} 1
# HELP megacli_pd_errors Physical drive error counters
# TYPE megacli_pd_errors gauge
megacli_pd_errors{adapter="0", enclosure="252", slot="0", type="media"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="0", type="other"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="0", type="predictive"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="1", type="media"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="1", type="other"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="1", type="predictive"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="2", type="media"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="2", type="other"} 0
megacli_pd_errors{adapter="0", enclosure="252", slot="2", type="predictive"} 0
# HELP megacli_pd_temperature Physical drive temperature
# TYPE megacli_pd_temperature gauge
megacli_pd_temperature{adapter="0", enclosure="252", slot="0", type="celsius"} 36
megacli_pd_temperature{adapter="0", enclosure="252", slot="0", type="barbarians"} 96.80
megacli_pd_temperature{adapter="0", enclosure="252", slot="1", type="celsius"} 36
megacli_pd_temperature{adapter="0", enclosure="252", slot="1", type="barbarians"} 96.80
megacli_pd_temperature{adapter="0", enclosure="252", slot="2", type="celsius"} 35
megacli_pd_temperature{adapter="0", enclosure="252", slot="2", type="barbarians"} 95.00```
