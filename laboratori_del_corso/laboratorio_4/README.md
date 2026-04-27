# IAM Authorization System — evoluzione del progetto

Questo laboratorio raccoglie una serie di script Python che mostrano, passo dopo passo, come costruire un sistema di autorizzazione `IAM` (Identity and Access Management) partendo da zero, aumentando progressivamente la complessità e la flessibilità.

---

## Panoramica degli step

| Step | Script | IAM | Concetto introdotto |
|------|--------|-----|---------------------|
| 0 | `step_0.py` | inline | dizionario Python + serializzazione JSON |
| 1 | `step_1.py` | `iam.json` | caricamento da file esterno |
| 2 | `step_2.py` | `iam.json` | refactor con funzione dedicata |
| 3 | `step_3.py` | `iam.json` | verifica autorizzazioni — match esatto |
| 3b | `step_3b.py` | `iam.json` | refactor con array di test |
| 4 | `step_4.py` | `iam.json` | match a prefisso sulle risorse |
| 5 | `step_5.py` | `iam_5.json` | permessi in doppio formato (stringa / oggetto) |
| 6 | `step_6.py` | `iam_6.json` | Ruoli utente e logica deny esplicito |

---

## step 0 — Dati inline e serializzazione JSON (`step_0.py`)

**obiettivo:** capire come Python e JSON si relazionano, e che la struttura dati è la stessa indipendentemente dal formato di serializzazione.

Questo è Il punto di partenza. Le autorizzazioni sono definite direttamente nel codice come dizionario Python, con una struttura che associa ogni utente a un insieme di risorse e relativi permessi.

```python
all_authorizations = {
    "ms@example.com": {
        "authorizations": {
            "S3::C8ABCX": { "perms": ["read", "write"] },
            "EC2::":       { "perms": ["read", "write", "delete"] }
        }
    }
}
```

Lo script mostra la conversione bidirezionale tra dizionario Python e stringa JSON (`json.dumps` / `json.loads`) e verifica che le due rappresentazioni siano equivalenti.


---

## step 1 — Caricamento da file esterno (`step_1.py`)

**obiettivo:** separare la configurazione dal codice. Il file `iam.json` è la fonte delle autorizzazioni, modificabile senza toccare il codice.

Le autorizzazioni sono spostate fuori dal codice e salvate in un file esterno `iam.json`. Lo script si limita a caricarlo con `json.load()`.

```python
with open("iam.json", encoding="utf-8") as f:
    all_authorizations = json.load(f)
```


---

## step 2 — Refactor con funzione dedicata (`step_2.py`)

**obiettivo:** buone pratiche di struttura del codice Python — funzioni riutilizzabili e punto di ingresso esplicito.

Il caricamento è incapsulato in una funzione `load_authorizations()`, e si introduce il pattern `if __name__ == "__main__"` per separare la logica eseguibile dal modulo riutilizzabile.

```python
def load_authorizations():
    with open("iam.json", encoding="utf-8") as f:
        return json.load(f)

def main():
    data = load_authorizations()

if __name__ == "__main__":
    main()
```

---

## step 3 — Verifica delle autorizzazioni con match esatto (`step_3.py`)

**obiettivo:** prima implementazione di un controllo di accesso. Gestione dei casi: utente inesistente, risorsa non autorizzata, permesso mancante.

Si introduce la funzione `check_authorization()`, che verifica se un utente ha un determinato permesso su una risorsa specifica.

```python
def check_authorization(all_authorizations, user_name, resource_name, required_permission):
    if user_name in all_authorizations:
        if resource_name in all_authorizations[user_name]["authorizations"]:
            if required_permission in all_authorizations[user_name]["authorizations"][resource_name]["perms"]:
                return True
    return False
```

Il match sulla risorsa è **esatto**: `"S3::C8ABCX"` corrisponde solo a `"S3::C8ABCX"`, non a `"S3::"`. Questo è il limite principale che sarà risolto nello step successivo.

---

## step 3b — Refactor con array di test (`step_3b.py`)

**obiettivo:** Raccogliere i test in un array e eliminare il codice ripetuto.

Rispetto a `step_3.py`, la logica di autorizzazione rimane identica. La novità è nel `main()`: i casi di test sono raccolti in un array di tuple e iterati con un ciclo `for`, eliminando la ripetizione del codice.

```python
tests = [
    ("an@other.com",    "",          ""),
    ("ms@example.com",  "S3::",      ""),
    ("ms@example.com",  "S3::C8ABCX", "read"),
    ("ms@example.com",  "S3::C8ABCX", "delete"),
]

for user_name, resource_name, action in tests:
    check_authorization(all_authorizations, user_name, resource_name, action)
```

---

## step 4 — Match del prefisso delle risorse (`step_4.py`)

**obiettivo:** modellare la gerarchia delle risorse cloud. In AWS, ad esempio, `"S3::"` rappresenta tutti i bucket S3, mentre `"S3::C8ABCX"` è un bucket specifico. Le regole più specifiche dovranno essere prioritarie.

Questo step risolve il limite del match esatto introducendo il **prefix matching**: una regola su `S3::` si applica a qualsiasi risorsa che inizi con `S3::`, come `S3::C8ABCX` o `S3::BUCKET42`.

```python
def match_resource(pattern, resource):
    return resource.startswith(pattern)
```

I pattern sono ordinati dal più specifico al più generico (per lunghezza decrescente), in modo che una regola più precisa abbia la precedenza:

```python
sorted_patterns = sorted(authorizations.keys(), key=len, reverse=True)
```

---

## step 5 — Doppio formato per i permessi (`step_5.py`)

**obiettivo:** evolvere il modello dati senza rompere la compatibilità con il formato precedente. Introduzione del concetto di **deny esplicito** come meccanismo di override.

E' introdotto un nuovo formato per i permessi, più espressivo, che affianca il formato semplice (stringa) già esistente:

**Formato semplice (precedente):**
```json
"perms": ["read", "write", "delete"]
```

**Formato oggetto (nuovo):**
```json
"perms": [
    {"action": "read",   "effect": "allow"},
    {"action": "delete", "effect": "deny"}
]
```

Il nuovo formato permette di esprimere **deny espliciti**, che hanno precedenza immediata su qualsiasi allow:

```python
if perm.get("effect") == "deny":
    return False   # blocca immediatamente
elif perm.get("effect") == "allow":
    allowed = True
```

Il file `iam_5.json` sfrutta questa nuova capacità: per `ms@example.com`, la risorsa `S3::C8ABCX` ha `delete` esplicitamente negato, mentre `read` e `write` sono permessi.

---

## step 6 — Ruoli e separazione utente/ruolo (`step_6.py`)

**obiettivo:** modellare il sistema di autorizzazioni di un cloud provider reale, in cui `utenti`, `ruoli` e `policy` interagiscono secondo un ordine di precedenza ben definito. Il deny esplicito a livello utente funziona come override delle permission ereditate dal ruolo.

E' lo step più complesso. Il modello dati è ristrutturato per supportare i **ruoli**: le autorizzazioni non sono più solo per singolo utente, ma possono essere ereditate da uno o più ruoli.

### Struttura di `iam_6.json`

```json
{
  "users": {
    "ms@example.com": {
      "roles": ["admin"],
      "authorizations": {
        "S3::C8ABCX": {
          "perms": [{"action": "delete", "effect": "deny"}]
        }
      }
    }
  },
  "roles": {
    "admin": {
      "authorizations": {
        "S3::": {
          "perms": [
            {"action": "read",   "effect": "allow"},
            {"action": "delete", "effect": "allow"}
          ]
        }
      }
    }
  }
}
```

### Logica di valutazione

La funzione `check_authorization()` segue questa priorità:

1. **Policy utente** — valutate per prime. Un deny esplicito blocca immediatamente tutto, senza consultare i ruoli.
2. **Policy dei ruoli** — valutate solo se le policy utente non hanno prodotto un deny esplicito. Un deny esplicito in un ruolo blocca tutto; un allow in almeno un ruolo concede l'accesso.
3. **Default deny** — se nessuna regola corrisponde, l'accesso è negato.

```
policy utente → deny esplicito?  →  DENY (fine)
                     ↓ no
             policy ruoli → deny esplicito?  →  DENY (fine)
                                ↓ no
                        almeno un allow?  →  ALLOW
                                ↓ no
                             DENY (default)
```
---

## Schema dell'evoluzione

```
step_0   Dati inline + JSON
   ↓
step_1   File esterno iam.json
   ↓
step_2   Refactor funzioni
   ↓
step_3   check_authorization() — match esatto
   ↓
step_3b  Test come array di dati
   ↓
step_4   Match a prefisso + ordinamento per specificità
   ↓
step_5   Doppio formato permessi + deny esplicito
   ↓
step_6   Ruoli + logica utente/ruolo
```

---

## File IAM

| File | Usato da | Caratteristiche |
|------|----------|-----------------|
| `iam.json` | step_1 → step_4 | Permessi come semplici stringhe |
| `iam_5.json` | step_5 | Permessi in formato oggetto `{action, effect}`, deny esplicito per risorsa specifica |
| `iam_6.json` | step_6 | Struttura separata `users` / `roles`, deny utente come override del ruolo |
