import subprocess
import re

def yesno(state):
    states = {
      "No": 0
    }
    return states.get(state, 1)

def state2int(state):
    #put remaining states here
    states = {
      "Online, Spun Up": 255
      }

    return states.get(state, 0)

def tobytes(inp):
    suffix=['kb','mb','gb','tb']
    i=0
    out=None
    inp=inp.strip().lower()

    while i < len(suffix):
        if re.search(suffix[i], inp):
            return float(inp.replace(suffix[i],'').strip()) * pow(1024, i+1)
        i+=1
    return inp

def main():
    info = subprocess.check_output(['/opt/MegaRAID/MegaCli/MegaCli64', '-AdpAllInfo', '-aAll', '-nolog']).decode('utf-8').splitlines()
    pdlist = subprocess.check_output(['/opt/MegaRAID/MegaCli/MegaCli64', '-PdList', '-aAll', '-nolog']).decode('utf-8').splitlines()
    global out
    out = {}
    adapter = None

    metrics= [
        'out["megacli_controller"]={ "help": "Controler information", "type": "gauge" , "metrics": []}',
        'out["megacli_controller_temperature_celsius"]={ "help": "ROC Temperature", "type": "gauge" , "metrics": []}',
        'out["megacli_memory_size_bytes"]={ "help": "Controler memory information", "type": "gauge" , "metrics": []}',
        'out["megacli_drives"]={ "help": "Drives information", "type": "gauge" , "metrics": []}',
        'out["megacli_memory_errors"]={ "help": "Memory errors", "type": "gauge" , "metrics": []}',
        'out["megacli_pd_info"]={ "help": "Physical drive detailed info", "type": "gauge" , "metrics": []}',
        'out["megacli_pd_temperature"]={ "help": "Physical drive temperature", "type": "gauge" , "metrics": []}',
        'out["megacli_pd_errors"]={ "help": "Physical drive error counters", "type": "gauge" , "metrics": []}',
        'out["megacli_pd_speed_bits"]={ "help": "Link and drive speed", "type": "gauge" , "metrics": []}'
    ]

    pat_info = [
        {
            'regex': re.compile(r'^Adapter\s+#\d+'),
            'action': [
                'adapter=line.split("#")[1].strip()'
            ]
        },
        {
            'regex': re.compile(r'^Product\s+Name\s+:'),
            'action': [
                'out["megacli_controller"]["metrics"].append({ "labels": { "adapter": adapter, "product_name": line.split(":")[1].strip()}, "val": 1})'
            ]
        },
        {
            'regex': re.compile(r'^FW\s+Package\s+Build\s*:'),
            'action': [
                'out["megacli_controller"]["metrics"].append({ "labels": { "adapter": adapter, "package_build": line.split(":")[1].strip()}, "val": 1 })'
            ]
        },
        {
            'regex': re.compile(r'^FW\s+Version\s+:'),
            'action': [
                'out["megacli_controller"]["metrics"].append({ "labels": { "adapter": adapter, "firmware_version": line.split(":")[1].strip()}, "val": 1 })'
            ]
        },
        {
            'regex': re.compile(r'^BIOS\s+Version\s+:'),
            'action': [
                'out["megacli_controller"]["metrics"].append({ "labels": { "adapter": adapter, "bios_version": line.split(":")[1].strip()}, "val": 1 })'
            ]
        },
        {
            'regex': re.compile(r'^Memory\s+Size\s+:'),
            'action': [
                'out["megacli_memory_size_bytes"]["metrics"].append({ "labels": { "adapter": adapter, "type": "Total memory" }, "val": tobytes(line.split(":")[1].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^ROC\s+temperature\s+:\s+\d+'),
            'action': [
                'out["megacli_controller_temperature_celsius"]["metrics"].append({ "labels": { "adapter": adapter, "type": "ROC temperature" }, "val": line.split(":")[1].split()[0].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Current\s+Size\s+of\s+FW\s+Cache\s+:'),
            'action': [
                'out["megacli_memory_size_bytes"]["metrics"].append({ "labels": { "adapter": adapter, "type": "Write cache" }, "val": tobytes(line.split(":")[1].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Virtual\s+Drives\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "virtual", "state": "Total" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^\s+Degraded\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "virtual", "state": "Degraded" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^\s+Offline\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "virtual", "state": "Offline" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Physical\s+Devices\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "physical", "state": "PhysicalTotal" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^\s+Disks\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "physical", "state": "DisksTotal"  }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^\s+Critical\s+Disks\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "physical", "state": "Critical"  }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^\s+Failed\s+Disks\s+:'),
            'action': [
                'out["megacli_drives"]["metrics"].append({ "labels": { "adapter": adapter, "type": "physical", "state": "Failed"  }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Memory\s+Correctable\s+Errors\s+:'),
            'action': [
                'out["megacli_memory_errors"]["metrics"].append({ "labels": { "adapter": adapter, "type": "correctable"  }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Memory\s+Uncorrectable\s+Errors\s+:'),
            'action': [
                'out["megacli_memory_errors"]["metrics"].append({ "labels": { "adapter": adapter, "type": "uncorrectable"  }, "val": line.split(":")[1].strip() })'
            ]
        },
    ]

    enclosure=None
    slot=None
    position=None
    device_id=None
    wwn=None

    pat_pd = [
        {
            'regex': re.compile(r'^Adapter\s+#\d+'),
            'action': ['global adapter ; adapter=line.split("#")[1].strip()']
        },
        {
            'regex': re.compile(r'^Enclosure\s+Device\s+ID:'),
            'action': ['enclosure=line.split(":")[1].strip()']
        },
        {
            'regex': re.compile(r'^Slot\s+Number\s*:'),
            'action': ['slot=line.split(":")[1].strip()']
        },
        {
            'regex': re.compile(r'^Drive\'s\s+position:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "disk_group"}, "val": line.split(":")[2].split(",")[0].strip() })',
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "span"}, "val": line.split(":")[3].split(",")[0].strip() })',
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "arm"}, "val": line.split(":")[4].split(",")[0].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Device\s+Id\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "device_id" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^WWN\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "wwn" }, "val": int(line.split(":")[1].strip(), 16) })'
            ]
        },
        {
            'regex': re.compile(r'^Sequence\s+Number\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "sequence_number" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Media\s+Error\s+Count\s*:'),
            'action': [
                'out["megacli_pd_errors"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "media" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Other\s+Error\s+Count\s*:'),
            'action': [
                'out["megacli_pd_errors"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "other" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Predictive\s+Failure\s+Count\s*:'),
            'action': [
                'out["megacli_pd_errors"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "predictive" }, "val": line.split(":")[1].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Raw\s+Size\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "size_raw" }, "val": tobytes(line.split(":")[1].split("[")[0].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Non\s+Coerced\s+Size\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "size_non_coerced" }, "val": tobytes(line.split(":")[1].split("[")[0].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Coerced\s+Size\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "size_coerced" }, "val": tobytes(line.split(":")[1].split("[")[0].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Firmware\s+state\s*:'),
            'action': [
                  'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "state" }, "val": state2int(line.split(":")[1].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Connected\s+Port\s+Number\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "port" }, "val": line.split(":")[1].split("(")[0].strip() })',
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "path" }, "val": line.split("path")[1].split(")")[0].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Needs\s+EKM\s+Attention\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "ekm_attention_needed" }, "val": yesno(line.split(":")[1].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Device\s+Speed\s*:'),
            'action': [
                'out["megacli_pd_speed_bits"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "drive" }, "val": tobytes(line.split(":")[1].split("/")[0].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Link\s+Speed\s*:'),
            'action': [
                'out["megacli_pd_speed_bits"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "link" }, "val": tobytes(line.split(":")[1].split("/")[0].strip()) })'
            ]
        },
        {
            'regex': re.compile(r'^Drive\s+Temperature\s*:'),
            'action': [
                'out["megacli_pd_temperature"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "celsius" }, "val": line.split(":")[1].split("C")[0].strip() })',
                'out["megacli_pd_temperature"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "barbarians" }, "val": line.split("(")[1].split(" ")[0].strip() })'
            ]
        },
        {
            'regex': re.compile(r'^Drive\s+has\s+flagged\s+a\s+S.M.A.R.T\s+alert\s*:'),
            'action': [
                'out["megacli_pd_info"]["metrics"].append({ "labels": { "adapter": adapter, "enclosure": enclosure, "slot": slot, "type": "smart_alert" }, "val": yesno(line.split(":")[1].strip()) })'
            ]
        },
    ]

    for m in metrics:
        exec(m)

    global line
    for line in info:
        for p in pat_info:
            if p['regex'].match(line):
                for a in p['action']:
                    exec(a, globals())
                continue

    for line in pdlist:
        for p in pat_pd:
            if p['regex'].match(line):
                for a in p['action']:
                    exec(a, globals())
                continue

#  print json.dumps(out, indent=2, sort_keys=True)
    for k,v in iter(out.items()):
        print("# HELP " + k + " " + v['help'])
        print("# TYPE " + k + " " + v['type'])
        for m in v['metrics']:
            print ( str(k) + '{' + ', '.join([ "{}=\"{}\"".format(str(l),str(m['labels'][l])) for l in sorted(m['labels']) ]) + '} ' +  str(m['val']) )

if __name__ == "__main__":
    main()
