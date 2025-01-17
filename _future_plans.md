# Future Plans for next release:
- Big ideas:
	- Docker container to make it more plug and play as well as it being identical on each run and on multiple machines.
	- Live ISO version?
- Improvements:
	- analyses everything in a folder (same as iso and future zip)
	- Extracting archives and looking at the files inside
	- More sophisticated scanning of the files especially for all the non-singed files
		- To use as services
			- https://github.com/VirusTotal/yara-python (IN Assemblyline 4)
			- https://github.com/hiddenillusion/AnalyzePE	(Old 10+ years and only python code maybe add as a service?)
			- http://www.openvas.org/ - https://github.com/greenbone/openvas-scanner (Already works in container should make it work in Assemblyline 4)
		- Do not think fits this use case
			- https://github.com/keithjjones/malgazer (Think this is just a machine learning algorithm to classify malware not detect?)
			- https://github.com/joxeankoret/pyew
	- Use Assemblyline 4 to check and validate code (https://github.com/CybercentreCanada/assemblyline-base)
		- Services:
			- AntiVirus
			- CAPA
			- CAPE
			- Espresso
			- Extract
			- Floss
			- FrankenStrings
			- JsJaws
			- MetaPeek
			- Oletools
			- PeePDF
			- TagCheck
			- Unpacker
			- ViperMonkey
			- XLMMacroDeobfuscator
			- YARA
		- Community Services
			- ClamAV
			- WindowsDefender
	- support of ~~online and~~ offline installation of OST, meaning whole system including OS in a VM environment
		- .OVA and step-by-step installation
		- air gapped updater for definition files and so on needs to exist

	- Installation metod
		- [Ansible](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/index.html)
		- Security/vuln scan of the docker images with [trivy](https://github.com/aquasecurity/trivy)
		- [Hardening guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
		- [CIS Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
			- [CIS tester](https://github.com/aquasecurity/kube-bench)
			- [Red Team/pentest kubernetes cluster](https://github.com/aquasecurity/kube-hunter)
		- [Kubernetes set up with ansible](https://github.com/techno-tim/k3s-ansible)

## Flow

- Flow for: Open Source Tvätt - Analysis of Signature Code, Hash, And Malware (OST ASCHAM)
	1. python start script
		```
		INPUT
			scan type
				file
				folder
			input file
			type
				Microsoft
				Red Hat
				Ubuntu
				VMWare
			hash
		OUTPUT
			result.csv
		STEPS
			- take and validate user inputs
			- verify hash
			- generate hash
			- prepare for containers
				- mounts iso (if applicable)
				- create relevant dirs
				- copy files to working dirs
			- builds container
			- start container (series? or parallel?)
			- gather results from all containers and generate result.csv
		```
	2. signature container
		```
		INPUT
			scan folder
			type
				Microsoft		(microsoft Container [Fedora])
				Red Hat			(RPM container [Fedora])
				Ubuntu			(deb container [Ubuntu]+[Microsoft])
				VMWare			(?)
			var WORKIGNDDIR = ./output/{type}/{file name}/{date}/
		OUTPUT
			signature_result.csv
			WORKIGNDDIR/signature.*
		STEPS
			- runs the scripts similar to it works today but with Extracting functionality
			- generate signature_result.csv
		```
	3. Script scan container
		```
		INPUT
			scan folder
			var WORKIGNDDIR = ./output/{type}/{file name}/{date}/
		OUTPUT
			script_result.csv
			WORKIGNDDIR/script.*
		STEPS
			- analyses script files
			- generate script_result.csv
		```
	4. Bad code container
		```
		INPUT
			scan folder
			var WORKIGNDDIR = ./output/{type}/{file name}/{date}/
		OUTPUT
			malware_result.csv
			WORKIGNDDIR/malware.*
		STEPS
		- analyses malware signature
		```
	6. wait for user to look at results before killing container

## ToDo

1. [x] Find software and functions for:
	- [x] Script Analysis
	- [x] Bad code / Malware Analysis
2. [ ] Containers
	- [ ] Build the python code to work in containers
	- [ ] Migrate the containers to Assembly line 4 services
	- [ ] Port other projects to work in Assembly line 4
3. ...
4. [ ] Profit

