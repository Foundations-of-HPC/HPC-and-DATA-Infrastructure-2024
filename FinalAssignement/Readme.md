# HPC and Data infrastructure final assignement

**Everybody has a testing environment. Some people are lucky enough enough to have a totally separate environment to run production in.**

In many environments, having a dedicated testing setup (separate from production) is essential for developing and experimenting with new ideas—without disrupting live systems. To facilitate this, we have created **Virtual Orfeo**, a testing environment designed to closely replicate the core features of our production HPC cluster.

Virtual Orfeo offers:
- The same authentication and identity management via **FreeIPA**, which integrates the login across all nodes and services.
- A **Slurm** controller deployed through **k3s** (a lightweight Kubernetes distribution).
- A login node and compute nodes resembling those in the production environment.

The repository for Virtual Orfeo, including deployment instructions, can be found here:
<https://gitlab.com/area7/datacenter/codes/virtualorfeo>

## Overview of Virtual Orfeo

1. **Authentication**
   Virtual Orfeo uses **FreeIPA** to handle user authentication across compute nodes, login node, and Slurm containers. FreeIPA is installed on a dedicated VM, allowing centralized user and group management through a web UI. When a new user is added, changes are propagated automatically to all components.

2. **Container-Orchestrated Slurm**
   The **k3s** Kubernetes distribution runs on a dedicated virtual machine (`kube01`), hosting the key Slurm components:
   - **slurmdbd** for accounting
   - **slurmctld** for scheduling

   For more information on Slurm components, see:
   <https://github.com/Foundations-of-HPC/HPC-and-DATA-Infrastructure-2024/blob/main/tutorials/slurm/slurm.md> and follow the official documentations.

3. **Compute Nodes**
   Virtual Orfeo includes one login node (`login01`) and two compute nodes (`node01` and `node02`), organized into three partitions:
   - **debug**
   - **p1**
   - **p2**

   While these partitions are not intended for heavy computations, they allow for testing and experimentation with job scheduling and HPC configuration.

## Virtual Machines
   After deploying Virtual Orfeo (by following the provided README), you will have a set of VMs with these IP addresses:

   - `kube01` at `192.168.132.10`
   - `login01` at `192.168.132.50`
   - `node0[1,2]` at `192.168.132.[51,52]`
   - `ipa01` at `192.168.132.70` (hosts FreeIPA; web GUI at <https://ipa01.virtualorfeo.test/ipa/ui/>).
     - If the GUI is not reachable, add `192.168.132.70 ipa01.virtualorfeo.test` to `/etc/hosts`.

All of these VMs are defined within the **vagrantfiles** folder.

## Overview of OrfeoKubOverlay

Alongside the `virtualorfeo` repository our testing infrastructure includes also the following one:

<https://gitlab.com/area7/datacenter/codes/orfeokuboverlay>

In OrfeoKubOverlay repository are stored all the manifests, values file and charts used to properly configure the `kube01` machine mentioned above.

In particular, the following services are hosted in Kubernetes:

 - `cert-managert`: a simple to use tool which manages all the certificates in the Kuberentes cluster, ensuring secure connection between the services.
 - `prometheus & grafana` as monitoring tools to keep track of the cluster status.
 - `MinIO` is an object storage solution compatible with the Amazon S3 API,
 - `authentik` used as a centralized user management and an API for single sign-on (SSO).

In principle Authentik software has the capability to manage users and groups by itself however, since the FreeIPA is already in place, we will use the FreeIPA as the main source of truth for the users and groups, letting Authentik to authenticate the users against the FreeIPA.
This is done through LDAP queries.

The monitoring aspect is out of the scope of this exam, while all the other services is going to be needed.

## Tasks

You can refer to [this quick-start guide](https://gitlab.com/IsacPasianotto/testing-env-doc) to deploy a working testing infrastructure as starting point for the task that you will be asked to solve.
Note that, differently from the given example, in which only the `ipa01` and `kube01` node are used, you will need to have the entire virtualorfeo environment up and running!

### HPC-infrastructure assignments

#### 1. Implement Distributed Storage with Ceph
Your first task is to set up a **Ceph**-based distributed storage system within Virtual Orfeo, mirroring the approach used in the production environment. The main steps include:

---
1. **VM Planning**
   Define an **odd number** of VMs to ensure high availability in a Ceph cluster (e.g., 3 or 5).

2. **Add Storage**
   Attach additional storage disks to these VMs to serve as **OSD**.

3. **Deploy a Ceph Cluster**
   Install and configure Ceph across the VMs.

4. **Create a Replicated Pool and File System**
   Once the cluster is up, create a replicated pool and then set up a Ceph file system.

5. **Mount the File System**
   Mount the Ceph file system on all nodes (e.g., at `/orfeo/cephfs/scratch`).

Optionally, you can use **Ansible** to automate some or all of these steps, such as mounting the file system on each node.
More details can be found in `ceph-deploy.md`, which follows the deployment approach introduced in the lectures.

#### 2. Enhance Slurm Configuration
The current Slurm configuration is minimal and simply queues jobs in submission order. Your second task is to modify this configuration to resemble a production-like environment by introducing **Quality of Service (QOS)** rules. Specifically:

- **Implement a Debug QOS**:
  Create a high-priority QOS (for example, `orfeo_debug`) that allows short, resource-light jobs to run with high priority regardless of submission order.

  For instance, if jobs `job1`, `job2`, `job3` were submitted, followed by a debug job `dbg1` (with `--qos=orfeo_debug`), the debug job should preempt or be scheduled before the other queued jobs, provided it meets the debug QOS criteria (e.g., minimal resources and short runtime).

You can modify the Slurm configuration by:
- Editing files directly in the **`slurmctld`** pod, or
- Updating the **`slurm-conf`** ConfigMap in the Kubernetes cluster.

To inspect the cluster, log into `kube01` and use **`k9s`** to browse the pods and ConfigMaps.

### Data-infrastructure tasks


#### 3. Deploy and Test the OFED Environment

Complete the deployment and testing of the OFED virtual environment, which includes MinIO and Authentik.
The testing process involves verifying that Authentik and MinIO work correctly, with **both*** a **graphical** login and **API-based access**, utilizing credentials managed by Authentik.

#### 4. File Synchronization

Nomad Oasis is a data management platform that allows users to store and share files.
Since It has its own storage system, it is necessary to synchronize MinIO storage with the Nomad Oasis database.

Deploy Nomad Oasis [following the instructions in the repository](https://github.com/FAIRmat-NFDI/nomad-distro-template?tab=readme-ov-file#deploying-the-distribution)

Design a synchronization procedure between files stored in MinIO and Nomad Oasis, leveraging the APIs provided by both services. The goal is to create an automated mechanism for updating and sharing files.

---

### Deliverables

By the end of this assignment, you should have:

1. A **Ceph** cluster deployed within the Virtual Orfeo environment, with a replicated pool and file system mounted on all nodes.
2. An updated **Slurm** configuration that supports a debug QOS, enabling high-priority scheduling of qualifying short jobs.
3. A well-documented file where you show that you were able to login into MinIO through the Authentik service for an user that you have enrolled in FreeIPA. For what regard the API-based method, feel free to attach any script needed to achieve this result.
4. A synchronization procedure (ideally a script) that allows to download a file from MinIO and upload it to Nomad Oasis and vice versa.

### Computational resources
Because the virtual environment requires significant RAM and CPU resources, a dedicated virtual machine will be provided for your assignments. If you have any questions, concerns, or difficulties, please feel free to reach out at any time.
