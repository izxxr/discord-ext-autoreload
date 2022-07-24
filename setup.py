from setuptools import setup

with open("README.MD", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()


setup(name='discord-ext-autoreload',
      author='nerdguyahmad',
      url='https://github.com/nerdguyahmad/discord-ext-autoreload',
      version="0.1.1",
      packages=['discord.ext.autoreload'],
      long_description=long_description,
      license='MIT',
      description='A discord.py extension that allows automatic hot-reloading of extensions',
      install_requires=install_requires,
      python_requires='>=3.5.3'
)
