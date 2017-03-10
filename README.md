# gencfg

A Python (works in both 2 and 3) script that applies csv data to configuration templates (in jinja2 format).

## Requirements

- [Python](https://www.python.org/) **3.x**
- [Jinja2](http://jinja.pocoo.org/)

To install dependencies, run `pip install -r requirements.txt` after cloning the repo (or `pip3` if running under python3).

## Usage

Script has two modes:

1. Generate a `csv` header from a template file: `t.py csvheader -t template.j2`
2. Generate device configuration based on a template and data: `t.py gencfg -t template.j2 -d data.csv`

The `csv` file MUST have a header row defining the variables used in the template and all of the variables must be present. Any extra columns will be ignored.

## Example

With the template in `example.j2`:

```
!
hostname {{ROUTER_HOSTNAME}}
!
!
no ip domain lookup
no ip http server
no ip http secure-server
ip ssh source-interface Loopback0
ip ssh version 2
!
!
ip vrf {{VRF_NAME}}
 description {{CUSTOMER_NAME}} {{VRF_NAME}}
!
!
interface Loopback0
 description Management interface
 ip vrf forwarding {{VRF_NAME}}
 ip address {{PRIMARY_MGMT_LOOPBACK}} 255.255.255.255
!
```

And data in `example.csv`:

```
ID,CUSTOMER_NAME,PRIMARY_MGMT_LOOPBACK,ROUTER_HOSTNAME,VRF_NAME
1,Mega Super Market,10.0.255.1,msmarket-brtr-1,MSM
2,Mega Super Market,10.0.255.2,msmarket-brtr-2,MSM
3,Mega Super Market,10.0.255.3,msmarket-brtr-3,MSM
4,Mega Super Market,10.0.255.4,msmarket-brtr-4,MSM
5,Mega Super Market,10.0.255.5,msmarket-brtr-5,MSM
6,Mega Super Market,10.0.255.6,msmarket-brtr-6,MSM
7,Mega Super Market,10.0.255.7,msmarket-brtr-7,MSM
8,Mega Super Market,10.0.255.8,msmarket-brtr-8,MSM
9,Mega Super Market,10.0.255.9,msmarket-brtr-9,MSM
10,Mega Super Market,10.0.255.10,msmarket-brtr-10,MSM
```

The result of running `t.py gencfg -t example.j2 -d example.csv` will be `10` files in the `config` subdirectory. For example, `cfg-4` will contain:

```
!
hostname msmarket-brtr-4
!
!
no ip domain lookup
no ip http server
no ip http secure-server
ip ssh source-interface Loopback0
ip ssh version 2
!
!
ip vrf MSM
 description Mega Super Market MSM
!
!
interface Loopback0
 description Management interface
 ip vrf forwarding MSM
 ip address 10.0.255.4 255.255.255.255
```
