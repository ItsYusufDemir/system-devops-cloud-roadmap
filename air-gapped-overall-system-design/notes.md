# Info
- in this section, I will design secure, optimized, HA air-gapped systems in overoll.

# Notes

- We simulate air-gapped system here via CDR and DLP transfer simulators.

## Nexus

- Nexus in air-gapped system.

- There is a repo hosted type named air-gapped-pypi. When user enters pip install x, request sent to the smart_proxy script. It checks first nexus, if nexus does not have, creates a request to the high_side_in. Then dlp transfer it to the low_side_out. Then low side agent watches the directory and when it sees new request, it downloads the python package to the low_side_in. Then cdr transfers it to the high_side_out. Lastly, high_side_uploader watches that file and uploads it to the nexus.
- if the user try again, she can now able to download it via nexus.

## Internal Network

- all communication between servers must have encrpyted. Suppose we have a nginx gateway and it forwards traffic to other servers. Suppose we have https between client and nginx gateway. We also must https between nginx gateway and other servers. To do that we setup nginx to other server too. We also setup a interncal Certificate Authority (CA). Then we implement mTLS between gateway and other servers so that no unencrypted traffic.