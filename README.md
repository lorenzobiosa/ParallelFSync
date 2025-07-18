# ParallelFSync

**ParallelFSync** è un sistema modulare ad alte prestazioni per la sincronizzazione continua tra due filesystem NFS remoti.  
Supporta sincronizzazione delta, eliminazione file mancanti, scansione e trasferimento in parallelo tramite `rsync`.

---

## 📦 Caratteristiche

- Sincronizzazione **continua** in background
- Supporta **NFS o qualsiasi filesystem montato**
- Utilizza `mtime` e `size` per rilevare modifiche
- Elimina file rimossi dalla sorgente
- **Parallelismo massivo** in fase di scansione e rsync
- Logging avanzato su file
- Interamente scritto in Python (>= 3.7)

---

## ⚙️ Requisiti

- Python **3.7+**
- `rsync` installato sul sistema
- Filesystem montati localmente:
  - `/mnt/source_nfs` → sorgente
  - `/mnt/target_nfs` → destinazione
- Permessi di scrittura su:
  - `/var/log/parallel_fsync.log`
  - Destinazione di sync

---

## 📁 Struttura del progetto

```
ParallelFSync/
├── config.py        # Configurazione generale
├── logger.py        # Logging su file
├── scanner.py       # Scansione file system multi-thread
├── syncer.py        # Rsync parallelo dei file modificati
├── deleter.py       # Rimozione file eliminati
├── main.py          # Ciclo principale asincrono
```

---

## 🚀 Installazione

1. **Estrai l'archivio:**
   ```bash
   tar -xvzf ParallelFSync.tar.gz
   cd ParallelFSync
   ```

2. **Installa i requisiti Python (se serve):**
   ```bash
   pip install -r requirements.txt  # se usi logging avanzato, altrimenti non necessario
   ```

3. **Verifica che `rsync` sia disponibile:**
   ```bash
   rsync --version
   ```

4. **Modifica il file `config.py` se necessario:**
   ```python
   SOURCE = "/mnt/source_nfs"
   DEST = "/mnt/target_nfs"
   ```

---

## ▶️ Avvio

Esegui lo script principale:
```bash
python3 main.py
```

Per eseguirlo in background:
```bash
nohup python3 main.py &
```

---

## 📝 Log

Il file di log si trova in:
```
/var/log/parallel_fsync.log
```

---

## 🛠️ Configurazione avanzata (`config.py`)

| Parametro               | Descrizione                                           |
|-------------------------|-------------------------------------------------------|
| `SOURCE`                | Percorso della directory sorgente                     |
| `DEST`                  | Percorso della directory di destinazione              |
| `BATCH_SIZE`            | N. massimo di file per batch rsync                    |
| `MAX_PARALLEL_RSYNC`    | N. massimo di rsync concorrenti                       |
| `DEBOUNCE_SECONDS`      | Attesa tra due scan successive                        |
| `DELETE_INTERVAL_SECONDS` | Frequenza del controllo file eliminati            |
| `INCLUDE_PATTERNS`      | Lista di pattern da includere (es. `["*.txt"]`)       |
| `EXCLUDE_PATTERNS`      | Lista di pattern da escludere                         |

---

## 🧪 Test suggeriti

- Prova a modificare, aggiungere e rimuovere file dalla sorgente e verifica:
  - che i file vengano copiati nella destinazione
  - che i file rimossi vengano eliminati
  - che il log mostri le azioni eseguite

---

## 📄 Licenza

Questo progetto è distribuito senza licenza specifica (default closed).  
Contattami per uso commerciale o integrazione in infrastrutture enterprise.

---
