from setuptools import setup

setup(name='discord-ext-autoreload',
      author='nerdguyahmad',
      url='https://github.com/nerdguyahmad/discord-ext-autoreload',
      version="0.1.0",
      packages=['discord.ext.autoreload'],
      license='MIT',
      description='A discord.py extension that allows automatic hot-reloading of extensions',
      install_requires=['discord.py>=1.7'],
      python_requires='>=3.5.3'
)
