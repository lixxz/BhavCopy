# Bhav Copy
- Django webapp which downloads bhavcopy from BSE's website daily. 
- Vue frontend where entries can be searched and exported to a CSV file.
- Redis is used for data storing and celery beat for task scheduling.

## Screenshot
![Demo](image.PNG)

## Setup Instructions
To run the app locally, follow these steps:
1. Clone the repository:
```
git clone https://github.com/lixxz/BhavCopy.git
cd Bhavcopy/
```

2. Create and activate virtualenv(Python 3.6+):
```
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Install and start redis(for ubuntu):
```
sudo apt install redis-server
redis-server --port 6379
```

5. Start the celery beat scheduler and worker:
```
celery -A bhavcopy worker -B
```

6. Run the django server:
```
python manage.py runserver 8000
```
App should be accessible now at http://localhost:8000