ittc-server-django
==================

## Description

This repository contains a Django server for running ITTC applications.  This application provides a Django interface for managing an in-memory tile cache and translator.  The application acts like a proxy and translates between tile schemas if possible.  For example, you can service tiles in TMS, TMS-Flipped, and Bing formats while only saving tiles on disk in one format when using `ittc-server-django` as a proxy/cache.

### CyberGIS
The Humanitarian Information Unit has been developing a sophisticated geographic computing infrastructure referred to as the CyberGIS. The CyberGIS provides highly available, scalable, reliable, and timely geospatial services capable of supporting multiple concurrent projects.  The CyberGIS relies on primarily open source projects, such as PostGIS, GeoServer, GDAL, OGR, and OpenLayers.  The name CyberGIS is dervied from the term geospatial cyberinfrastructure.

## Installation

As root (`sudo su -`), execute the following commands:

```
apt-get update
apt-get install -y curl vim git nginx
apt-get install -y memcached zlib1g-dev libjpeg-dev rabbitmq-server
apt-get install -y libapache2-mod-python python-dev python-pip
pip install django
pip install django-cors-headers
pip install Pillow
pip install umemcache
pip install django-memcached-pool 
pip install gunicorn
pip install greenlet
pip install gevent
#pip install celery
#Need to use fork of celery that support ultramemcached ("umemcache")
#Workaround <--
#pip install git+git://github.com/celery/py-amqp.git
#pip install git+git://github.com/celery/billiard.git
#pip install git+git://github.com/celery/kombu.git
#pip install --upgrade kombu
pip install git+git://github.com/state-hiu/celery.git@umemcache
#-->
```

Then, as ubuntu, execute the following commands:

```
cd ~
git clone https://github.com/state-hiu/ittc-server-django.git ittc-server-django.git

```
Then, update SITEURL (e.g., http://hiu-maps.net/) in settings.py:

```
vim ittc-server-django.git/ittc/ittc/settings.py
```

## Usage

The application can be run through the Django built-in development server or Gnuicron ([http://gunicorn.org/](http://gunicorn.org/)).

You first need to start 3 memcached instances with the following commands  The settings.py assumes the default cache is running on port 11211, the cache for the tiles is running on port 11212, and the cache for Celery results is running on port 11213.

```
memcached -vv -m 128 -p 11211 -d
memcached -vv -m 1024 -p 11212 -d
memcached -vv -m 128 -p 11213 -d
```

Then, prepare the server.

```
cd ittc-server-django.git/ittc
python manage.py syncdb
```

If `syncdb` asks if you would like to create an admin user, do it. 

Then start a Celery worker with:

```
cd ittc-server-django.git/ittc
celery -A ittc worker --loglevel=error
```

To run the application using the Django built-in development server, execute the following:

```
python manage.py runserver [::]:8000
```

To run the application using Gnuicorn, execute the following:

```
gunicorn --workers=4 --worker-class gevent -b 0.0.0.0:8000 ittc.wsgi
or
gunicorn --workers=4 --worker-class gevent -b unix:///tmp/gunicorn.sock --error-logfile error.log ittc.wsgi
```

You can learn more about gunicron configuration at [http://docs.gunicorn.org/en/develop/configure.html](http://docs.gunicorn.org/en/develop/configure.html).

### Heuristics

You can enable a variety of heuristics / branch prediction via the settings.py file.  The `nearby` heuristic caches all tiles at the same level within the radius distance (distance 1 --> 3*3 tiles, distance 2 = 25 tiles, distance 3 = 25 tiles).  The `up` heuristic caches all tiles parent to a requested tile.  The `down` heuristic caches tiles that are `children` to the requested tile within the depth and minZoom/maxZoom range.  For instance, if you request a tile at 14 and have a depth of 2, all the children tiles from 14 to 16 will be requested.

```
ITTC_SERVER = {
    'name': 'HIU Imagery Services',
    'cache': {
        'memory': {
            'enabled': True,
            'size': 1000,
            'minZoom': 0,
            'maxZoom': 14
        }
    },
    'heuristic': {
        'down': {
            'enabled': True,
            'depth': 1,
            'minZoom': 0,
            'maxZoom': 18
        },
        'up': {
            'enabled': True
        },
        'nearby': {
            'enabled': True,
            'radius': 2
        }
    }
}
```

## Contributing

HIU is currently accepting pull requests for this repository. Please provide a human-readable description of the changes in the pull request. Additionally, update the README.md file as needed.

## License
This project constitutes a work of the United States Government and is not subject to domestic copyright protection under 17 USC § 105.

However, because the project utilizes code licensed from contributors and other third parties, it therefore is licensed under the MIT License. http://opensource.org/licenses/mit-license.php. Under that license, permission is granted free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the conditions that any appropriate copyright notices and this permission notice are included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
