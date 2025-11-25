import csv
from datetime import datetime
from .models import Expense, Sector, Way

def get_date_from_the_file(csvfile):
    print(f"Processing file: {csvfile}")
    
    # Check if file is CSV (simple check based on extension provided by UploadedFile object usually, 
    # but here csvfile might be a path string or file object depending on how it's passed)
    # In views.py, it seems to be passed as a file path or object.
    # Let's assume it's a path for now as per original code, but views.py might need checking.
    
    records_created = 0
    
    try:
        # If csvfile is a file-like object (from request.FILES), we need to handle it differently
        # But original code treated it as a path 'filepath = form.cleaned_data["csvfile"]' 
        # which suggests it might be saved to disk first or it's a path string.
        # However, standard Django FileField cleaned_data is a FieldFile object.
        # Let's assume we open it in text mode.
        
        # If it's a path string:
        if isinstance(csvfile, str):
            f = open(csvfile, "r", encoding="utf-8")
        else:
            # If it's an UploadedFile object, we need to decode it
            from io import TextIOWrapper
            f = TextIOWrapper(csvfile.file, encoding="utf-8")

        reader = csv.DictReader(f)
        
        for row in reader:
            # Parse date
            date_str = row.get("DATEINFO")
            # Assuming date format is YYYY-MM-DD based on original SQL
            
            # Get or create related objects if necessary, or just use IDs if they match
            # Original SQL used SECTOR_ID and WAY_ID directly.
            # We should check if we need to fetch instances.
            sector_id = row.get("SECTOR")
            way_id = row.get("WAY")
            
            sector = None
            if sector_id:
                sector = Sector.objects.filter(id=sector_id).first()
                
            way = None
            if way_id:
                way = Way.objects.filter(id=way_id).first()

            Expense.objects.create(
                dateinfo=date_str,
                place=row.get("PLACE"),
                cost=row.get("COST"),
                summary=row.get("SUMMARY"),
                isfixed=bool(int(row.get("ISFIXED", 0))),
                # creationinfo is auto_now=True, so we don't set it manually usually, 
                # but if we want to preserve legacy creation time we might need to change model field
                # For now let's let Django set it to now, or if we really need to import it:
                # creationinfo=row.get("CREATIONINFO") 
                sector=sector,
                way=way
            )
            records_created += 1
            
        if isinstance(csvfile, str):
            f.close()
            
        print(f"Successfully inserted {records_created} records.")
        
    except Exception as e:
        print(f"Error importing data: {e}")
        raise e

