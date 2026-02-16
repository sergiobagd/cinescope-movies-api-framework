import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Model for JSON
class DateTimeRequest(BaseModel):
    currentDateTime: str # Format: "2025-02-13T21:43Z"

# Holidays list in Russia (example)
russian_holidays = {
    "01-01": "Новый год",
    "01-07": "Рождество Христово",
    "02-23": "День защитника Отечества",
    "03-08": "Международный женский день",
    "05-01": "Праздник Весны и Труда",
    "05-09": "День Победы",
    "06-12": "День России",
    "11-04": "День народного единства",
    "12-31": "Канун Нового года"
}

@app.post("/what_is_today")
def what_is_today(request: DateTimeRequest):
    try:
        # Parse data from incoming JSON
        date_str = request.currentDateTime
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")

        # Get month and day in format "MM-DD"
        month_day = date_obj.strftime("%m-%d")

        # Check if there is holiday in this date
        holiday = russian_holidays.get(month_day, "Today there is no holiday in Russia")

        return {"message": holiday}
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect date format. Use format 'YYYY-MM-DDTHH:MMZ'.")

@app.get("/ping")
def ping():
    return "PONG!"

# Server launching
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=16002)

