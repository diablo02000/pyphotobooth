# PhotoBooth

![Photobooth icons](photobooth/img/photobooth.png)

## Description

Create your own photobooth.

## Requirements

### Hardware

This project was build with:

- Raspberry B+
- SD Card
- Pi camera
- Pi Touchscreeen Display

### Software

First you need to install `Raspbian` on your SD card.
I will not explain this section, they are plenty of tutorial
to do this.

Then we need to install `python` and `python pip` on your Raspbian:

```shell
~# apt-get install python3 python3-pip
```

Run the requirements installation:

```shell
~$ pip3 install -r requirements.txt
```

And add the last python3 librairies:

```shell
~# apt-get install python3-picamera python3-pip python3-tk python3-pil.imagetk libatlas-base-dev
```

## Troubleshoot

### libcblas import error

```
ImportError: libcblas.so.3: cannot opne shared object file: No such  file or directory
```

You maybe forget to install `libatlas-base-dev`:

```shell
install apt-get install libatlas-base-dev
```

### ImageTk import error

```
ImportError: cannot import name 'ImageTk'
```

You aybe forget to install `python3-pil.imagetk`:

```shell
apt-get install python3-pil.imagetk
```
