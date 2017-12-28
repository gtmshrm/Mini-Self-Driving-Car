# Self driving car - Robot

## [Real-time and Simulation videos](https://www.youtube.com/playlist?list=PLdB2BCvl7RPBdJyfz71QX25x7unK-nBI8)

## File structure

```bash
+-- rasp-pi
|   +-- collect_data
|   |   +-- <data collections modules>
|   +-- +-- client.py
|   |
|   +-- preprocess
|   |   +-- data_preprocess.py, merge_and_prep.py
|   +-- +-- server.py
|   |
|   +-- selfdrive
|   |   +-- <self driving modules>
|   |   ...
```

## Collect data

  + Drive the car around the track and collect driving data
    Read README.md of: ./raspi-pi/collect_data


## Preprocess

  + Preprocess the train to be consumped by the model
    Read README.md of: ./server/preprocess


## Train

  + Train the model
    Read README.md of: ./selfdrive


## Test

### On Simulation

  + Test results of pre-trained model on simulation
    Read README.md of: ./selfdrive

### In Real-time

  + Test results of pre-trained model in real time
    Read README.md of: ./rasp-pi
    Read README.md of: ./server

## Note: Use GPU in real-time predictions otherwise the prediction would be badly hindered

  + Server with gpu:
    Entire process of image transmission and steering angle prediction takes about <= 0.1 seconds per frame

  + Server with cpu:
    Entire process of image transmission and steering angle prediction takes about 0.6-0.8 seconds per frame
