# adblock-compiler-python (Bind DNS)
Python script to compile adblock dns rpz zone file for use in Bind

# Introduction

This is a helper script that helps you compile a list of adblock domains into a single list. It then formats them into a single zone file, for use in an adblock dns server. This file is meant to be used as a RPZ zone file in Bind DNS server.

This makes it easy for the user to compile its own custom list, use custom blacklist sources, add whitelisting, and add custom domain overrides.

## Input sources

This script sources its adblock lists from the following locations:

### Web host sources

Web sources are taken from the `data/blacklist-src-urls.txt` file. This script will fetch the list from the urls in that file, extract the domains and include them in the adblock list.

### Local blacklist

This is taken from files in `data/blacklist.d` directory. Domains are extracted from the files and included in the adblock list.

### Local overrides

This is taken from files in `data/overrides.d` directory. Files in this entry typically contain the bind zone entries. These are injected directly into the final adblock zone file.

### Local whitelist

This is taken from files in `data/whitelist.d` directory. Domains are extracted from these files, and they are filtered out from the final adblock list.

## Output file

The output of this script, is a single Bind zone file at `data/output.d/blacklist.zone`.

A sample output looks as follows:
```
$TTL 1H
@               SOA     LOCALHOST. named-mgr.example.com (1 1h 15m 30d 2h)
                NS      LOCALHOST.

duckduckgo.com      CNAME   safe.duckduckgo.com.
www.duckduckgo.com  CNAME   safe.duckduckgo.com.
google.com          CNAME   forcesafesearch.google.com.
www.google.com      CNAME   forcesafesearch.google.com.
www.bing.com        CNAME   strict.bing.com.

zedo.com            A       0.0.0.0
doubleclick.net     A       0.0.0.0
```

# How To Use

## Running the script

1. You need to have `pipenv` and `python3` in your system.

2. Install the dependencies
```
pipenv install
```

3. Running the script
```
pipenv run python src/main.py
```

4. The output file will be at `data/output.d/blacklist.zone`.

5 You can customize the input lists and sources to your needs.

## Using the output zone file in Bind

The output `blacklist.zone` file is used as an RPZ zone file in Bind dns server. A typical config may look as follows:

1. file: `/etc/bind/blacklist.zone` contains the generated zone file

2. file: `/etc/bind/named.conf.local`
```
zone "blacklist" {type master; file "/etc/bind/blacklist.zone"; allow-query {none;}; };
```

3. file: `/etc/bind/named.conf.options`
```
options {
    directory "/var/bind";
    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    forward only;
    dnssec-validation auto;
    recursion yes;
    auth-nxdomain no;    # conform to RFC1035
    listen-on-v6 { any; };
    allow-query { any; };
    response-policy { zone "blacklist"; };
};
```
