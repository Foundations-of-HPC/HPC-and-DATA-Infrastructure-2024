# Ceph deploy 

## Bootstrap the first ceph node

- `dnf install -y ceph-base ceph-common ceph-volume podman`
- `systemctl enable --now podman`
- `systemctl enable --now chronyd`
- `dnf install cephadm -y`
- `cephadm bootstrap --mon-ip {{ip-address}}`
- `ceph config set mgr mgr/dashboard/server_addr {{ip-address-dashboard}}`
- `ceph dashboard set-grafana-api-url {{grafana-address}}`
-  copy `/etc/ceph/ceph.pub` to all ceph nodes
-  Eventually if necessary `ceph-volume lvm zap /dev/sd* --destroy` to clear devices

Expand the cluster
```
ceph orch host add cephXX {{ip-address}}
```


## Create fs
```
$ ceph fs volume create testfs
```

Create rule:

```
ceph osd crush rule create-replicated replicated_rule_ssd_host default host ssd
ceph osd crush rule create-replicated replicated_rule_hdd_host default host hdd
```

Create pool:

```
ceph osd pool create testfs.data.replica1 replicated_rule_hdd_host
ceph osd pool create testfs.data.replica2 replicated_rule_hdd_host
ceph osd pool create testfs.data.replica3 replicated_rule_hdd_host
```

Set pool size:
```
ceph config set global  mon_allow_pool_size_one true
ceph osd pool set testfs.data.replica1 size 1 --yes-i-really-mean-it
ceph osd pool set testfs.data.replica2 size 2
ceph osd pool set testfs.data.replica3 size 3
```

## Mount on client

- `echo "{{ceph-admin-secret}}" > testfs.secret && chmod 660 testfs.secret`
- `mkdir /mnt/testfs &&  echo "10.128.6.215:6789,10.128.6.216:6789,10.128.6.217:6789,10.128.6.218:6789:/ /mnt/testfs ceph fs=testfs,name=admin,secretfile=/etc/ceph/testfs.secret,read_from_replica=balance,noatime,_netdev,defaults 0 0" >> /etc/fstab`

Add datapool to benchmark fs
```
ceph fs add_data_pool testfs testfs.data.replica1
ceph fs add_data_pool testfs testfs.data.replica2
ceph fs add_data_pool testfs testfs.data.replica3
```

Bind the folder to replicated pool:
```
setfattr -n ceph.dir.layout.pool -v testfs.data.replica1 replica1
setfattr -n ceph.dir.layout.pool -v testfs.data.replica2 replica2
setfattr -n ceph.dir.layout.pool -v testfs.data.replica3 replica3
```

Check with:
```
$ ceph fs ls
name: testfs, metadata pool: cephfs.testfs.meta, data pools: [cephfs.testfs.data testfs.data.replica1 testfs.data.replica2 testfs.data.replica3 ]
```


