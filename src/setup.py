from setuptools import setup, find_packages

install_requires = [
    'Django>=1.9.0,<1.10',
    'psycopg2==2.6.1',
    'gunicorn==19.3.0',
    'djangorestframework==3.2.2',
    'celery==3.1.19',
    'feedparser==5.2.1',
    'requests==2.9.1',
    'readability-lxml==0.6.1',
    'django-cors-headers==1.1.0',
]

setup(
    name='leth',
    version='0.0.1',
    description='Leth is a feed reader and read it later server',
    author='Greizgh',
    author_email='greizgh@ephax.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Topic :: Internet',
        'Topic :: Communications',
    ],
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True
)
