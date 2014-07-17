from distutils.core import setup

setup(
    name='NemPyCalibration',
    version='0.1.0',
    author='Valerie Simonis',
    author_email='valerie.simonis@gmail.com',
    packages=['nemPyCalibration', 'nemPyCalibration.test'],
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Useful things for nemPyCalibration.',
    long_description=open('README.txt').read(),
    install_requires=[
        "PyQt5 == 5.3.1",
        "cv2 >= 2.4.9",
    ],
)
