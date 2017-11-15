from setuptools import setup

setup(
    name='snipsmanagercore',
    version='0.1.5.9.9',
    description='The Snips manager core utilities for creating end-to-end assistants',
    author='Snips',
    author_email='labs@snips.ai',
    url='https://github.com/snipsco/snipsmanagercore',
    download_url='',
    license='MIT',
    install_requires=[
        'webrtcvad==2.0.10',
        'cython==0.21.1',
        'hidapi==0.7.99.post20',
        'paho-mqtt==1.3.0',
        'pyyaml==3.12',
        'pyaudio==0.2.8',
        'pygame==1.9.3',
        'pyusb==1.0.0',
        'snips-respeaker==0.6.2',
        'gTTS==1.2.2'
    ],
    test_suite="tests",
    keywords=['snips'],
    packages=[
        'snipsmanagercore'
    ],
    include_package_data=True,
)
