# McAfee WebGateway API List Update
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This simple python script allows you to update McAfee Web Gateway lists via the REST API.

## Prerequisites
Enable the McAfee WebGateway REST Interfaces under Configuration > User Interface.
Create a new user and assing appropriated policies to the user (including the REST Interface accessibility).

Update line 8 to 12 and update the list variable in line 79.

<img width="478" alt="screen shot 2018-08-08 at 16 17 51" src="https://user-images.githubusercontent.com/25227268/43842906-9fce52ac-9b26-11e8-8e6a-74611a0e3d36.png">

## Usage
```sh
python mwg.py <ip or domain>

e.g. python mwg.py 10.10.10.10
or
e.g. python mwg.py google.com
```

The script will perform the following actions:
1. Login - Create a new API session (cookie)
2. Get the ID to the List mentioned in line 79
3. Insert new entry
4. Commit changes
5. Logout

To see the changes in the McAfee Web Gateway UI click on Reload Data from Backend

![screen shot 2018-08-08 at 16 20 53](https://user-images.githubusercontent.com/25227268/43843096-0debc760-9b27-11e8-9b91-5f90dfe34efb.png)

This script can also be used in combination with the McAfee ESM to create right click actions to Block IP's or Domains.

## Global Blacklist 

Adding a client block list to the global blacklist 

```python
<entry>
    <id>com.scur.type.ip.316</id>
    <title>Blocked Clients</title>
    <type>com.scur.type.ip</type>
    <listType>ip</listType>
    <link href="https://mwg:4712/Konfigurator/REST/list/com.scur.type.ip.316" rel="self"/>
    <content>
        <list version="1.0.3.46" mwg-version="10.2.5-39162" name="Blocked Clients" id="com.scur.type.ip.316" typeId="com.scur.type.ip" classifier="Other" systemList="false" structuralList="false" defaultRights="2">
            <description>List of blocked client IPs</description>
            <content>
                <listEntry>
                    <entry>8.8.8.8</entry>
                    <description></description>
                </listEntry>
                <listEntry>
                    <entry>4.4.4.4</entry>
                    <description></description>
                </listEntry>
            </content>
        </list>
    </content>
</entry>
```
![Screenshot from 2022-04-20 23-06-17](https://user-images.githubusercontent.com/44593913/164237801-7943c39a-11dd-47a5-aba3-4ca98a750a01.png)


