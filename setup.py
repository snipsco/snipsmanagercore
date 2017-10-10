from setuptools import setup

setup(
    name='snipsskillscore',
    version='0.1.5.9.0',
    description='The Snips skills core utilities for creating end-to-end assistants',
    author='Michael Fester',
    author_email='michael.fester@gmail.com',
    url='https://github.com/snipsco/snips-skills-core',
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
        'snipsskillscore'
    ],
    include_package_data=True,
)
