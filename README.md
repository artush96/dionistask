# falcon + vue js

## Project setup

```
git clone https://github.com/artush96/dionistask.git
```

```
cd dionistask
```

## setup postgresql 

### install postgresql@10

#### create database db url = 'postgresql:///dionisdb' or edit db_connect.py and write your url


## setup falcon

###use python 3.7
```
python -m venv venv
```

#### activate venv

```
source venv/bin/activate
```

#### install req.txt

```
pip install -r req.txt
```

### run gunicorn server

```
gunicorn -b 127.0.0.1:8000 --reload app:app
```

#### create test data

```
cd tests
python worker.py
python activity_log.py
```

## setup vue app

```
cd vue-app
```

```
npm install
```

#### run vue server
```
npm run serve
```

### open npm serve url in browser

#### select date no less than date now and click Get Report

![Иллюстрация к проекту](https://github.com/artush96/dionistask/raw/master/images/date.png)

#### download button does not work correctly but pdf is created in the directory 'dionistask'

### api

#### api url = gunicorn server url '127.0.0.1:8000/api'

![Иллюстрация к проекту](https://github.com/artush96/dionistask/raw/master/images/postman.png)

![Иллюстрация к проекту](https://github.com/artush96/dionistask/raw/master/images/diagram.png)

![Иллюстрация к проекту](https://github.com/artush96/dionistask/raw/master/images/table.png)










