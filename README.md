# Logging network upload and download speed using `crontab`

First, install `speedtest-cli` using `pip` on `bash`:

``` bash
$ pip install speedtest-cli
```

Launch `crontab -e` on `bash` and add the following to the bottom of the file:

``` bash
# Log speed every 2 mins
*/5 * * * * { { date; /home/bharat.kunwar/Anaconda3/bin/speedtest --server 5833 --simple; } | tr '\n' ' '; echo; } >> /home/bharat.kunwar/Network/5min.log
```

Explanation:

- `*/5` means the command runs every 5 minutes
- Server 5833 is based in Newport. Do `speedtest --list` to lookup others.
- Command `tr` is used so that output can be logged to a single line.

# Visualising the generated log

Run the following on terminal. You may need to specify the path of the log file in `speed.py`.

```bash
$ python speed.py
```

The output will be available as `report.pdf`.