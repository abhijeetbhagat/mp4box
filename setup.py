from distutils.core import setup

setup(
    name='mp4box',
    version='0.1dev',
    packages=['mp4box',],
    package_data={'mp4box' : ['parsing/*.py', 'utils/*.py']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description='mp4 BMFF parsing lib'
)
