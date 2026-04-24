# Corso CS/2026

## Laboratori del corso

### Laboratorio 1

Creazione di uno script `Bash` da distribuire tra i server GNU/Linux per il backup del sistema in locale.\
Lo script è stato realizzato durante la lezione.

### Laboratorio 2

L'esercizio consiste nel generare, modificare, cancellare e gestire risorse sul provider `DigitalOcean` via `api` fornita dallo stesso cloud provider. La documentazione utilizzata è quella [ufficiale](https://docs.digitalocean.com/reference/api/).

Nella directory `laboratorio_2/` sono presenti:

1. esempio di `secrets` per il caricare nell'environment del token da utilizzare.
2. gli script suddivisi in step.

### Laboratorio 3

Realizzazione in load balancing di server web via `docker compose` e `nginx`.\
Per seguire i passaggi è possibile seguire in ordine le guide riportate di seguito:

1. [How to Install Docker on Ubuntu – Step-by-Step Guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
2. [Learn to build and deploy your distributed applications easily to the cloud with Docker](https://docker-curriculum.com/)
3. [How To Install and Use Docker Compose on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
4. [Samples overview](https://docs.docker.com/reference/samples)
5. [Load Balancing with Docker Compose and NGINX](https://medium.com/but-it-works-on-my-machine/load-balancing-with-docker-compose-and-nginx-b9077696f624)

### Laboratorio 4

Esercizio semplificato per il parsing di un `JSON` via `Python`. La struttura dati rappresenta un contenitore molto semplificato riconducibile ad un logica `RBAC` con `utenti`, `risorse` e `autorizzazioni`.\
Nella directory `laboratorio_4/` sono presenti:

1. il file`iam.json` per una versione semplificata di un generico framework `IAM`.
2. gli script suddivisi in step con complessità crescente.

## Laboratorio studenti

Le tracce fornite agli studenti sono riportate nel file [progetti_2026.pdf](laboratorio_studenti/progetti_2026.pdf).

Di seguito gli studenti che hanno optato per la discussione/realizzazione del progetto e la data di discussione della stessa.

| studenti | data discussione | progetto
|:---:|:---:|:---
| [Iacopo Somma<br/>Leonardo Barone](laboratorio_studenti/openvpn_vs_ikev2_vs_ipsec) | 20/04 | VPN panoramica generale e confronto tra OpenVPN, IKEv2 e IPSec
|[Francesco Bonanni<br/> Dennis Eremia](laboratorio_studenti/logserver) | 27/04 | Logserver
| [Donato Marchionda</br>Manuel Cilli](laboratorio_studenti/crittografia_dello_storage_1) | 27/04 | Crittografia dello storage e benchmark
| [Giorgio Di Donato](laboratorio_studenti/gre) | 4/05 | Protocollo GRE
| Francesca Di Giampaolo | ? | tunnel ssh
| [Matteo Corba](laboratorio_studenti/metodi_di_compressione) | 4/05 | metodi di compressione
| | | |
| [Alberto Cirillo](laboratorio_studenti/ansible) | 15/04 | Ansible
| [Anthony Candeloro](laboratorio_studenti/crittografia_dello_storage_0) | 15/04 | Crittografia dello storage e benchmark
| [Matteo Salis](laboratorio_studenti/crittografia_dello_storage_1) | 22/04 | crittografia dello storage
| [Simone Colazzilli](laboratorio_studenti/compressione_gzip_vs_zip) |  22/04 | compressione gzip/zip
| [Antonio Di Nucci](laboratorio_studenti/waf) | 22/04 | WAF
| [Samuele Lombardi](laboratorio_studenti/ipsec) | 22/04 | IPSec
| [Eleonardo Bajramovski](https://github.com/Neniku/Metodi_Di_Compressione/) | 22/04 | metodi di compressione
| [Lorenzo Delle Coste](laboratorio_studenti/load_balancer) | 22/04 | Load balancer
| Tommaso Tocco | 22/04 | container
| [Mario Marzia](laboratorio_studenti/sdn_vxlan) | 29/04 | SDN/VxLAN
| [Antonio Mascolo](laboratorio_studenti/algoritmi_raid) | 29/04 | analisi di algoritmi RAID
| [Francesco Cavaliere](laboratorio_studenti/filesystem_moderni) | 29/04 | filesystem moderni
