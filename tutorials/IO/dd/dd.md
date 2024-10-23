# Disk Benchmarking with `dd`

`dd` is a fundamental Linux command, primarily used for copying and converting files or data. While it isn't specifically designed for benchmarking, `dd` can be used to measure disk performance in some cases, particularly for sequential read and write speeds. In this tutorial, we will use `dd` to test sequential write speed.

## Sequential Write Speed Test

The following command writes data from `/dev/zero` to the device `/dev/sda`, bypassing any filesystem. This allows us to measure the raw performance of the device without filesystem overhead. The command writes a single block (`count=1`) of size 1MB (`bs=1M`).

```bash
# dd if=/dev/zero of=/dev/sda count=1 bs=1M
1+0 records in
1+0 records out
1048576 bytes (1.0 MB, 1.0 MiB) copied, 0.0237837 s, 44.1 MB/s
```

This small test is insufficient to achieve the maximum performance of the device. To identify the device model and characteristics, you can use the `smartctl` command:

```bash
$ smartctl -x /dev/sda
```

Sample output:

```
=== START OF INFORMATION SECTION ===
Vendor:               WDC
Product:              WUH722222AL5200
Revision:             WS03
User Capacity:        22,000,969,973,760 bytes [22.0 TB]
Logical block size:   512 bytes
Physical block size:  4096 bytes
Rotation Rate:        7200 rpm
Form Factor:          3.5 inches
Transport protocol:   SAS (SPL-4)
SMART support:        Available - device has SMART capability.
SMART support:        Enabled
```

By consulting the device's datasheet, we can see that this disk supports a sustained transfer rate of 291MB/s (277MiB/s) and a random read IOPS count of 212.



## Without Filesystem, HDD

To test the device’s performance more effectively, we can use a larger block size and transfer more data:

```bash
$ dd if=/dev/zero of=/dev/sda bs=1M count=5000
5000+0 records in
5000+0 records out
5242880000 bytes (5.2 GB, 4.9 GiB) copied, 21.9567 s, 239 MB/s
```

For a different device, using the `direct` flag to bypass caching:

```bash
$ dd if=/dev/zero of=/dev/sdb oflag=direct bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 30.7047 s, 273 MB/s
```

### With an XFS Filesystem, HDD

To test the performance while writing files to a filesystem, create an XFS filesystem on the disk:

```bash
$ mkfs.xfs /dev/sda
```

Mount the filesystem:

```bash
$ mkdir /mnt/mydisk
$ mount /dev/sda /mnt/mydisk
```

Now, writing a file on the filesystem will yield significantly higher performance, due to filesystem caching by the OS:

```bash
$ dd if=/dev/zero of=/mnt/mydisk/myfile bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 1.07404 s, 7.8 GB/s
```

This unusually high speed is due to the OS caching the writes. To get a more accurate result that reflects the actual write speed to disk, we can use the `direct` flag to bypass the cache:

```bash
$ dd if=/dev/zero of=/mnt/mydisk/myfile oflag=direct bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 31.8082 s, 264 MB/s
```

### With an EXT4 Filesystem, HDD

```bash
$ dd if=/dev/zero of=/mnt/mydisk/myfile  bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 30.3294 s, 277 MB/s

$ dd if=/dev/zero of=/mnt/mydisk/myfile oflag=direct  bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 35.6378 s, 235 MB/s
```

## NVME results

### No Filesystem, NVME

```bash
# dd if=/dev/zero of=/dev/nvme1n1   bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 4.40588 s, 1.9 GB/s
[root@ceph13 ~]# dd if=/dev/zero of=/dev/nvme1n1 oflag=direct  bs=1M count=16000
16000+0 records in
16000+0 records out
16777216000 bytes (17 GB, 16 GiB) copied, 3.40643 s, 4.9 GB/s
```

### XFS, NVME

```bash
$ dd if=/dev/zero of=/mnt/mydisk/myfile  bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 1.06052 s, 7.9 GB/s

$ dd if=/dev/zero of=/mnt/mydisk/myfile oflag=direct bs=1M count=8000
8000+0 records in
8000+0 records out
8388608000 bytes (8.4 GB, 7.8 GiB) copied, 1.65772 s, 5.1 GB/s
```


## Other Benchmarking Tools

While `dd` is useful for basic disk speed testing, it has limitations, particularly for modern SSDs and more complex workloads. For more comprehensive benchmarking, tools like **IOR**, **FIO**, and **IOzone** are recommended. These tools are optimized to test different I/O patterns, including random reads and writes, and they allow for multi-threaded benchmarking.

### Limitations of `dd`:

- **Single-threaded:** `dd` runs on a single thread, so the benchmark might be CPU-limited.
- **Sequential only:** It only tests sequential read/write speeds.
- **Limited data sources:** `dd` can only generate data from sources like `/dev/zero` or `/dev/random`.

For more details on why `dd` may not be an ideal benchmarking tool, check out [this article](https://blog.cloud-mercato.com/dd-is-not-a-benchmarking-tool/).


