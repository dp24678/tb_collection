from scheduler import scheduler_
from api.app import app




scheduler_.run()
app.run(host='0.0.0.0', port=5000)

