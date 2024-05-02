FROM python:3.10
WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements_mac.txt /app/requirements_mac.txt
RUN pip install -r requirements_mac.txt
COPY . /app
CMD ["funix", "app.py", "--port", "3000"]
