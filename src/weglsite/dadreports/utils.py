import csv
import io
from datetime import datetime, time, timedelta
from .models import CSVUpload, AsplayEntry

REQUIRED_COLUMNS = {'CUT', 'TITLE', 'ARTIST', 'ALBUM', 'GROUP', 'DATE', 'ACTSTART', 'ACTDUR'}

def parse_duration(val):
    if val is None or val is "":
        return timedelta()
    val = val.strip()
    parts = val.split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 2:
        return timedelta(minutes=parts[0], seconds=parts[1])
    elif len(parts) == 3:
        return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
    else:
        raise ValueError(f"Unrecognized duration format: '{val}'")
    
def parse_start_time(val):
    return datetime.strptime(val, "%H:%M:%S").time()

def parse_csv(file, filename):
    alreadyUploaded = False
    dupeFiles = CSVUpload.objects.filter(fileName=filename)
    for e in dupeFiles:
        if e.status is not "failed":
            alreadyUploaded = True

    if CSVUpload.objects.filter(fileName=filename).exists() and not alreadyUploaded:
        raise ValueError(f"'{filename}' has already been uploaded.")

    upload = CSVUpload.objects.create(fileName=filename, status="pending")

    try:
        text = io.TextIOWrapper(file, encoding='cp1252')
        reader = csv.DictReader(text)

        if not REQUIRED_COLUMNS.issubset(set(reader.fieldnames or [])):
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            raise ValueError(f"CSV is missing required columns: {missing}")
        
        entries = []
        for i, row in enumerate(reader, start=2):
            try:
                entries.append(AsplayEntry(
                    upload = upload,
                    cutID = row["CUT"].strip(),
                    artist = row["ARTIST"].strip(),
                    title = row["TITLE"].strip(),
                    album = row['ALBUM'].strip(),
                    group = row['GROUP'].strip(),
                    startTime = parse_start_time(row['ACTSTART']),
                    durationSeconds = parse_duration(row['ACTDUR']),
                    playDate = datetime.strptime(row['DATE'].strip(), '%m/%d/%Y').date()
                )) 
            except (ValueError, KeyError) as e:
                #raise ValueError(f"Error on row {i}: {e}")
                next(reader)
            
        AsplayEntry.objects.bulk_create(entries, batch_size=500)

        upload.rowCount = len(entries)
        upload.status = "success"
        upload.save()

    except Exception:
        upload.status = "failed"
        upload.save()
        raise

    return upload