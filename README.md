# Self driving car for GSOC 2017

## File structure

```bash
+-- rasp-pi
|   +-- collect_data
|   |   +-- <data collections modules>
|   +-- +-- client.py
|   +-- preprocess
|   |   +-- data_preprocess.py, merge_and_prep.py
|   +-- +-- server.py
|   |   +-- <data collections modules>
|   +-- selfdrive
|   |   +-- <self driving modules>
|   |   ...
```

## Collect data

  + Drive the car around the track and collect driving data
    Read README.md of: raspi-pi/collect_data

## Train

  + Train the model
