# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9

EXPOSE 8000
WORKDIR /code
# Install pip requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

# Give execution rights on the cron scripts
RUN chmod +x /code/app/test_cron.py

#Install Cron
RUN apt-get update && apt-get install nano cron -y

# Add the cron job
RUN chmod 0644 /code/app/scrapping.py

# Adding crontab to the appropriate location
ADD ./app/crontab /etc/cron.d/crontab

# Giving permission to crontab file
RUN chmod 0644 /etc/cron.d/crontab

#start service
RUN service cron start

# # Running crontab
RUN crontab /etc/cron.d/crontab

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000","--root-path","/api/dwp_jobs"]

#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]